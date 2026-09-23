"""Tests for the configuration module.

These tests assert only the public ``Settings`` behavior shared by both the
pydantic-settings and stdlib backends, so they hold regardless of the
``include_pydantic_settings`` choice. The one backend-specific detail is
``.env`` isolation in ``test_defaults`` — only the pydantic-settings backend
reads a dotenv file.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from hwid.__metadata__ import PROJECT_NAME
from hwid.core.config import Settings
from hwid.core.dirs import ROOT_FOLDER_PATH

if TYPE_CHECKING:
    from pathlib import Path

# Mirror the prefix the implementation derives from the project name.
ENV_PREFIX = f"{PROJECT_NAME.upper().replace('-', '_')}_"


def test_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Settings expose the documented defaults when no env vars are set."""
    for name in ("DEBUG", "LOG_LEVEL", "CONFIG_DIR"):
        monkeypatch.delenv(f"{ENV_PREFIX}{name}", raising=False)

    settings = Settings()

    assert settings.debug is False
    assert settings.log_level == "INFO"
    assert settings.config_dir == ROOT_FOLDER_PATH


def test_log_level_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    """The log level is read from the prefixed environment variable."""
    monkeypatch.setenv(f"{ENV_PREFIX}LOG_LEVEL", "DEBUG")

    assert Settings().log_level == "DEBUG"


def test_config_dir_env_override(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The config directory is read from the prefixed environment variable."""
    monkeypatch.setenv(f"{ENV_PREFIX}CONFIG_DIR", str(tmp_path))

    assert Settings().config_dir == tmp_path


@pytest.mark.parametrize("value", ["1", "true", "YES", "on", "y"])
def test_debug_truthy(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    """Recognized truthy strings enable debug mode (case-insensitively)."""
    monkeypatch.setenv(f"{ENV_PREFIX}DEBUG", value)

    assert Settings().debug is True


@pytest.mark.parametrize("value", ["0", "false", "no", "off"])
def test_debug_falsy(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    """Recognized falsy strings disable debug mode."""
    monkeypatch.setenv(f"{ENV_PREFIX}DEBUG", value)

    assert Settings().debug is False
