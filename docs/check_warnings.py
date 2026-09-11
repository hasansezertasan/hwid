"""Fail the docs build on any Sphinx warning not in the expected allowlist.

The ``docs-build`` tox env builds with ``-w docs/_build/warnings.txt`` (Sphinx
writes its warning stream to that file instead of ``-W`` turning the first
warning into a hard error). This script then owns the pass/fail decision: it
diffs the emitted warnings against the committed ``expected_warnings.txt``
allowlist and fails on BOTH unexpected new warnings AND expected warnings that
are no longer emitted (so the allowlist can't silently rot).

The healthy default is an empty ``expected_warnings.txt`` — zero tolerated
warnings. When a genuinely-unavoidable upstream warning appears, add its exact
(normalized) line to the allowlist in the same PR: an explicit, reviewable act
rather than a wholesale ``suppress_warnings`` hack.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
EMITTED = HERE / "_build" / "warnings.txt"
EXPECTED = HERE / "expected_warnings.txt"


def normalize(text: str) -> set[str]:
    """Split a warning stream into machine-independent, comparable lines.

    Absolute path prefixes are stripped back to the ``docs/`` segment so the
    allowlist is portable across machines and CI checkouts. Backslash separators
    are folded to ``/`` first so a warning located on Windows normalizes to the
    same line an allowlist entry recorded on Linux/CI does. The ``/docs/``
    marker (with a leading separator) is used so an ancestor directory whose
    name merely contains ``docs`` (e.g. a repo cloned into ``some-docs/`` or
    under ``~/docs/``) is not mistaken for the source segment. Blank lines and
    ``#`` comment lines (allowlist header only — Sphinx never emits them) are
    ignored.

    Returns:
        The set of normalized, non-empty, non-comment warning lines.
    """
    lines: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # Fold Windows backslash separators to "/" so a warning located on
        # Windows matches an allowlist entry recorded on Linux/CI.
        line = line.replace("\\", "/")
        # Strip to the last "docs/" source segment. Anchoring on "/docs/"
        # ignores ancestor dirs that merely contain "docs"; the leading
        # separator is dropped so already-relative "docs/..." lines pass
        # through unchanged.
        idx = line.rfind("/docs/")
        lines.add(line[idx + 1 :] if idx != -1 else line)
    return lines


def main() -> int:
    """Diff emitted warnings against the allowlist and report the verdict.

    Returns:
        ``0`` when the emitted warnings exactly match the allowlist, ``1`` when
        there are unexpected or missing warnings.
    """
    emitted = (
        normalize(EMITTED.read_text(encoding="utf-8")) if EMITTED.exists() else set()
    )
    expected = (
        normalize(EXPECTED.read_text(encoding="utf-8")) if EXPECTED.exists() else set()
    )
    unexpected = emitted - expected
    missing = expected - emitted
    for warning in sorted(unexpected):
        print(f"::error::unexpected sphinx warning: {warning}")
    for warning in sorted(missing):
        print(f"::error::expected sphinx warning no longer emitted: {warning}")
    if unexpected or missing:
        print(
            f"docs warning gate FAILED: "
            f"{len(unexpected)} unexpected, {len(missing)} missing "
            f"(see docs/expected_warnings.txt)",
            file=sys.stderr,
        )
        return 1
    print("docs warning gate OK: emitted warnings match the allowlist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
