"""Tests for the directory configuration module."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

from hwid.core.dirs import _resolve_home, _root_folder_base

if TYPE_CHECKING:
    import pytest


def test_resolve_home_returns_real_home() -> None:
    """When the home directory is resolvable, it is returned as-is."""
    assert _resolve_home() == Path.home()


def test_resolve_home_returns_none_when_undeterminable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unresolvable home directory yields ``None`` instead of raising."""

    def _raise() -> Path:
        msg = "Could not determine home directory."
        raise RuntimeError(msg)

    monkeypatch.setattr(Path, "home", staticmethod(_raise))

    assert _resolve_home() is None


def test_root_folder_base_prefers_home() -> None:
    """A resolvable home directory is used as the root folder base."""
    home = Path("/home/example")

    assert _root_folder_base(home) == home


def test_root_folder_base_falls_back_to_temp_dir() -> None:
    """A missing home directory falls back to the OS temp directory."""
    assert _root_folder_base(None) == Path(tempfile.gettempdir())
