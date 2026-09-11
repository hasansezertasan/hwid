"""Keep the Python modules embedded in the documentation executable."""

from __future__ import annotations

import importlib.util
from importlib.metadata import version
from pathlib import Path
from typing import TYPE_CHECKING

from hwid.__metadata__ import PROJECT_NAME

if TYPE_CHECKING:
    from types import ModuleType

EXAMPLES_DIR = Path(__file__).parents[1] / "docs" / "examples"


def _load_example(path: Path) -> ModuleType:
    """Import one documentation example directly from its source path."""
    spec = importlib.util.spec_from_file_location(f"docs_example_{path.stem}", path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_documentation_examples_are_importable() -> None:
    """Every nested Python module in ``docs/examples`` imports successfully."""
    examples = sorted(EXAMPLES_DIR.rglob("*.py"))
    assert examples, "docs/examples must contain at least one tested module"
    for path in examples:
        _load_example(path)


def test_version_lookup_example_uses_the_installed_distribution() -> None:
    """The usage-page example resolves the same version as package metadata."""
    example = _load_example(EXAMPLES_DIR / "version_lookup.py")
    assert example.version_lookup() == version(PROJECT_NAME)
