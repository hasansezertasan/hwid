"""Configurations for the project."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path

from hwid.__metadata__ import PROJECT_NAME
from hwid.core.dirs import ROOT_FOLDER_PATH

# Dashes are normalized to underscores so the prefix is a valid shell variable
# name (e.g. ``my-project`` -> ``MY_PROJECT_``).
_ENV_PREFIX = f"{PROJECT_NAME.upper().replace('-', '_')}_"

# Values (case-insensitive) accepted as boolean true, matching pydantic's
# bool coercion so both Settings variants behave identically.
_TRUTHY = {"1", "true", "yes", "on", "y", "t"}


def _env(name: str, default: str) -> str:
    """Read a prefixed environment variable, falling back to a default.

    Args:
        name: The unprefixed setting name (e.g. ``"LOG_LEVEL"``).
        default: The value to use when the variable is unset.

    Returns:
        str: The environment value, or ``default`` if it is not set.
    """
    return os.environ.get(f"{_ENV_PREFIX}{name}", default)


@dataclass(frozen=True)
class Settings:
    """Application settings sourced from environment variables.

    Stdlib-only fallback used when pydantic-settings is not enabled. Each field
    is overridable via an environment variable named after the uppercased
    project name (dashes normalized to underscores) plus the field, for
    example ``MY_PROJECT_LOG_LEVEL``.
    """

    # Example settings - replace or extend these with your project's own.
    # ``log_level`` is consumed by ``core/logging_setup.py``; ``debug`` and
    # ``config_dir`` are illustrative placeholders not yet wired into anything.
    debug: bool = field(default_factory=lambda: _env("DEBUG", "").lower() in _TRUTHY)
    log_level: str = field(default_factory=lambda: _env("LOG_LEVEL", "INFO"))
    config_dir: Path = field(
        default_factory=lambda: Path(_env("CONFIG_DIR", str(ROOT_FOLDER_PATH)))
    )


@cache
def get_settings() -> Settings:
    """Return the cached settings singleton.

    Cached so all callers share one instance; tests can reset or override it
    via ``get_settings.cache_clear()`` instead of patching an import-time value.

    Returns:
        Settings: The cached settings instance.
    """
    return Settings()


__all__ = ["Settings", "get_settings"]
