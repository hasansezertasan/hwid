"""Pytest configuration shared across the test suite.

Auto-applies a per-component marker to each test based on its top-level
``tests/<dir>/`` directory, so ``pytest -m web`` (or ``-m "not web"``) selects a
component without per-test decoration. Markers are registered in pyproject.toml
``[tool.pytest.ini_options] markers``. See issue #160 / ADR-028.

Also keeps the Markdown doctest surface to the single root ``README.md``: see
``collect_ignore_glob`` below.

Also hosts the ``missing_metadata`` fixture: every component degrades or fails
differently when the package metadata is unreadable, but they all read it
through ``core.app``, so one fixture covers every component's error path
(ADR-033).
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from hwid.core import app as service

if TYPE_CHECKING:
    from importlib.metadata import Distribution

# ``--doctest-glob=README.md`` (pyproject ``addopts``) matches on the *basename*,
# so without this every ``tests/**/README.md`` -- fixture notes, a subdirectory
# guide -- would also be collected as a doctest the moment it contained a ``>>>``
# line. The root README is the whole Markdown doctest surface (ADR-028); prose
# under tests/ stays prose.
collect_ignore_glob = ["*.md"]


# tests/<dir> names that map to a component marker, rendered from the enabled
# components. An unmarked dir (e.g. a future one) is simply left unmarked.
# `# fmt: off` keeps this one-per-line no matter how many components are enabled:
# the generated ruff config sets skip-magic-trailing-comma, so an unguarded set
# literal would otherwise collapse or explode purely by line width.
# fmt: off
_COMPONENT_DIRS: frozenset[str] = frozenset({
    "core",
    "cli",
})
# fmt: on


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """Mark each collected test with its top-level tests/<dir> component name."""
    tests_root = Path(str(config.rootpath)) / "tests"
    for item in items:
        try:
            rel = item.path.relative_to(tests_root)
        except ValueError:  # pragma: no cover - defensive: items are under tests/
            continue
        component = rel.parts[0] if len(rel.parts) > 1 else "core"
        # Every hwid tests/<dir> is a component today, so the unmarked branch
        # only runs once a non-component dir is added.
        if component in _COMPONENT_DIRS:  # pragma: no branch
            item.add_marker(component)


class _MissingDistribution:
    """Stub whose ``from_name`` always reports missing package metadata."""

    @staticmethod
    def from_name(name: str) -> Distribution:
        """Fail the way an uninstalled or partial package does.

        Args:
            name: The distribution name that cannot be found.

        Raises:
            PackageNotFoundError: Always.
        """
        raise PackageNotFoundError(name)


@pytest.fixture
def missing_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make the shared app service behave as if the package were not installed.

    Every component reads the version through ``core.app``, so patching it here
    reaches the CLI's exit-1 path, the web app's 503 responses, the MCP tool's
    error text and the GUI/TUI "unknown" degradation alike.

    ``monkeypatch`` reverses the patch at teardown, so nothing is yielded.
    """
    monkeypatch.setattr(service, "Distribution", _MissingDistribution)
