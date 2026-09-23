"""Directory configurations for the project."""

import tempfile
from pathlib import Path

from hwid.__metadata__ import PROJECT_NAME


def _resolve_home() -> Path | None:
    """Return the user's home directory, or ``None`` if it is undeterminable.

    ``Path.home()`` raises ``RuntimeError`` when the home directory cannot be
    resolved (``HOME`` unset and no passwd entry -- some containers, service
    accounts, sandboxes). This module is imported at startup, so letting that
    propagate would crash even read-only commands like ``--help`` or
    ``version``. Return ``None`` instead and let callers decide how to degrade.

    Returns:
        Path | None: The home directory, or ``None`` when it is undeterminable.
    """
    try:
        return Path.home()
    except RuntimeError:
        return None


def _root_folder_base(home: Path | None) -> Path:
    """Return the base directory that holds the project's root folder.

    Falls back to the temp directory when ``home`` is ``None`` purely so
    module-level paths stay valid ``Path`` objects for callers that need *a*
    location (e.g. the illustrative ``config_dir`` setting). Nothing in the
    template writes to that fallback automatically -- file logging is skipped
    entirely when the home directory is unresolvable (see ``HOME_IS_RESOLVABLE``
    and ``core/logging_setup.py``), because a predictable shared path would let
    another local user hijack the log file.

    Args:
        home: The resolved home directory, or ``None`` if undeterminable.

    Returns:
        Path: ``home`` when available, otherwise the OS temp directory.
    """
    if home is not None:
        return home
    return Path(tempfile.gettempdir())


_HOME = _resolve_home()

HOME_IS_RESOLVABLE: bool = _HOME is not None
"""Whether the user's home directory could be resolved at import time.

When ``False`` the project has no user-owned directory to write to, so file
logging is disabled in ``core/logging_setup.py`` rather than falling back to a
predictable shared location.
"""

ROOT_FOLDER_NAME: str = f".{PROJECT_NAME}"
"""Name of the root folder."""
ROOT_FOLDER_PATH: Path = _root_folder_base(_HOME) / ROOT_FOLDER_NAME
"""Path to the root folder."""
LOG_FILE_PATH: Path = ROOT_FOLDER_PATH / "main.log"
"""Path to the log file."""
CONFIG_FILE_PATH: Path = ROOT_FOLDER_PATH / "config.json"
"""Path to the config file."""
