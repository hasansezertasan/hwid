"""Build versioned documentation and assemble the full GitHub Pages site.

Only the *current* release is built here; every previously published version is
copied across from the ``gh-pages`` branch untouched — old versions are never
rebuilt. The version list is derived from the ``gh-pages`` directory listing, so
there is no committed ``versions.json`` to maintain. See ADR-027.

Usage::

    DOCS_BUILD_VERSION=0.3.1 python tools/build_docs.py site

Run inside the docs environment (``uv run --group docs ...``) so ``sphinx-build``
and the docs dependencies are importable.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import subprocess  # noqa: S404
import sys
import tarfile
from pathlib import Path

from packaging.version import InvalidVersion, Version

# Version-directory granularity, baked from the Copier ``docs_version_granularity``
# answer. Edit here only if you want to change how release versions map to docs
# directories: "minor" -> X.Y, "major" -> X, "full" -> X.Y.Z.
VERSION_GRANULARITY = "minor"

DOCS_DIR = Path("docs")
HTML_DIR = DOCS_DIR / "_build" / "html"
WARNINGS_FILE = DOCS_DIR / "_build" / "warnings.txt"
VERSIONS_JSON = DOCS_DIR / "_static" / "versions.json"

# gh-pages refs to try, in order (a local branch after ``git fetch origin
# gh-pages:gh-pages``, or the remote-tracking ref after a plain fetch).
GH_PAGES_REFS = ("gh-pages", "origin/gh-pages")

# Raised when the required release version is not supplied via the environment.
_MISSING_VERSION_MSG = "DOCS_BUILD_VERSION is required"

_REDIRECT_HTML = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url=./latest/">
    <title>Redirecting to the latest documentation</title>
  </head>
  <body>
    Redirecting to the <a href="./latest/">latest documentation</a>.
  </body>
</html>
"""


def slugify(version: str) -> str:
    """Reduce a release version to its docs-directory slug.

    Args:
        version: The release version, e.g. ``0.3.1`` (a leading ``v`` is
            tolerated).

    Returns:
        The version-directory slug at the configured granularity, e.g. ``0.3``
        (minor), ``0`` (major), or ``0.3.1`` (full).
    """
    parts = version.lstrip("v").split(".")
    if VERSION_GRANULARITY == "major":
        return parts[0]
    if VERSION_GRANULARITY == "minor":
        return ".".join(parts[:2])
    return version.lstrip("v")


def _is_version_dir(name: str) -> bool:
    """Report whether a gh-pages entry name is a published version directory.

    Args:
        name: A top-level name from the gh-pages tree.

    Returns:
        ``True`` if ``name`` parses as a PEP 440 version (so ``latest``,
        ``pr-preview``, ``_static``, ``index.html`` etc. are excluded).
    """
    try:
        Version(name)
    except InvalidVersion:
        return False
    return True


def _gh_pages_ref() -> str | None:
    """Resolve which gh-pages ref is available.

    Returns:
        The first gh-pages ref that resolves, or ``None`` if none exist.
    """
    for ref in GH_PAGES_REFS:
        result = subprocess.run(  # noqa: S603
            ["git", "rev-parse", "--verify", "--quiet", ref],  # noqa: S607
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            return ref
    return None


def existing_versions() -> list[str]:
    """List the version slugs already published on the gh-pages branch.

    Returns:
        The numeric version-directory names found on gh-pages (empty if the
        branch does not exist yet).
    """
    ref = _gh_pages_ref()
    if ref is None:
        return []
    result = subprocess.run(  # noqa: S603
        ["git", "ls-tree", "--name-only", ref],  # noqa: S607
        capture_output=True,
        text=True,
        check=True,
    )
    return [name for name in result.stdout.split() if _is_version_dir(name)]


def pick_latest(slugs: list[str]) -> str:
    """Choose the ``latest`` alias target.

    Prereleases (``rc``/``a``/``b``/``dev`` slugs, which only appear under
    ``full`` granularity) are excluded so a pre-release never becomes ``latest``
    while any stable version exists.

    Args:
        slugs: All known version slugs.

    Returns:
        The highest stable slug, or the highest overall if all are prereleases.
    """
    stable = [slug for slug in slugs if not Version(slug).is_prerelease]
    return max(stable or slugs, key=Version)


def write_versions_json(slugs: list[str], latest: str) -> None:
    """Write the switcher manifest that ``conf.py`` reads into ``html_context``.

    Args:
        slugs: All known version slugs (including the one being built).
        latest: The slug the ``latest`` alias points at.
    """
    VERSIONS_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {"versions": sorted(slugs, key=Version, reverse=True), "latest": latest}
    VERSIONS_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_sphinx() -> None:
    """Run the same warning-gated build the docs-build tox env uses."""
    WARNINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-m",
            "sphinx",
            "-w",
            str(WARNINGS_FILE),
            "-b",
            "html",
            str(DOCS_DIR),
            str(HTML_DIR),
        ],
        check=True,
    )
    subprocess.run(  # noqa: S603
        [sys.executable, str(DOCS_DIR / "check_warnings.py")], check=True
    )


def preserve_from_gh_pages(name: str, out: Path, ref: str) -> None:
    """Extract the ``name`` subtree from gh-pages into ``out`` (keeping prefix).

    Args:
        name: The version-directory (or ``latest``) name to preserve.
        out: The assembled-site output directory to extract into.
        ref: The resolved gh-pages ref to read from.
    """
    archive = subprocess.run(  # noqa: S603
        ["git", "archive", ref, name],  # noqa: S607
        capture_output=True,
        check=False,
    )
    if archive.returncode != 0 or not archive.stdout:
        return  # not present on gh-pages (e.g. first release) — nothing to keep
    # Extract the in-memory tar with the stdlib so the script needs no external
    # ``tar`` binary. The stream is our own trusted ``git archive`` output; use
    # the safe extraction filter where available (Python 3.12+).
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tar:
        if sys.version_info >= (3, 12):
            tar.extractall(out, filter="data")
        else:
            tar.extractall(out)  # noqa: S202


def assemble_site(out: Path, slug: str, latest: str, all_slugs: list[str]) -> None:
    """Assemble ``out`` from the fresh build plus preserved prior versions.

    Args:
        out: The output directory to assemble the full site into.
        slug: The slug just built from the current release.
        latest: The slug the ``latest`` alias points at.
        all_slugs: Every known version slug.
    """
    out.mkdir(parents=True, exist_ok=True)
    (out / ".nojekyll").touch()
    (out / "index.html").write_text(_REDIRECT_HTML, encoding="utf-8")

    shutil.copytree(HTML_DIR, out / slug, dirs_exist_ok=True)
    if slug == latest:
        shutil.copytree(HTML_DIR, out / "latest", dirs_exist_ok=True)

    ref = _gh_pages_ref()
    if ref is None:
        return
    preserved = {s for s in all_slugs if s != slug}
    if slug != latest:
        preserved.add("latest")
    for name in preserved:
        preserve_from_gh_pages(name, out, ref)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Argument list to parse (defaults to ``sys.argv``).

    Returns:
        The parsed namespace with an ``output`` attribute.
    """
    parser = argparse.ArgumentParser(description="Assemble versioned docs site.")
    parser.add_argument("output", help="Directory to assemble the site into.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Build the current version and assemble the full versioned site.

    Args:
        argv: Argument list to parse (defaults to ``sys.argv``).

    Returns:
        A process exit code (``0`` on success).

    Raises:
        SystemExit: If ``DOCS_BUILD_VERSION`` is not set.
    """
    args = parse_args(argv)
    version = os.environ.get("DOCS_BUILD_VERSION", "").strip()
    if not version:
        raise SystemExit(_MISSING_VERSION_MSG)
    slug = slugify(version)

    all_slugs = sorted({*existing_versions(), slug}, key=Version)
    latest = pick_latest(all_slugs)
    write_versions_json(all_slugs, latest)

    # Tell conf.py which slug is being built so the switcher highlights it.
    os.environ["DOCS_BUILD_VERSION_SLUG"] = slug
    build_sphinx()

    assemble_site(Path(args.output), slug, latest, all_slugs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
