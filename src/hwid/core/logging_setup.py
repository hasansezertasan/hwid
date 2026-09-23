"""Set up logging for the project.

This module configures logging for the project, ensuring that
log handlers are only added once to prevent duplicate log entries if the
module is imported multiple times.

Setup is resilient to a read-only or unavailable ``$HOME``: if the log
directory cannot be created it degrades to console-only logging instead of
raising, so read-only commands (``--help``, ``version``) stay usable.

"""

import logging
import sys
from functools import cache
from logging.handlers import RotatingFileHandler

from hwid.__metadata__ import PROJECT_NAME
from hwid.core.config import get_settings
from hwid.core.dirs import HOME_IS_RESOLVABLE, LOG_FILE_PATH, ROOT_FOLDER_PATH

__all__ = ["get_logger", "setup_logger"]


def _resolve_level(name: str) -> int:
    """Translate a level name (e.g. ``"DEBUG"``) to its numeric value.

    Falls back to ``logging.INFO`` for unknown names so a bad config value
    never crashes logging setup. Because the fallback would otherwise be
    invisible (an operator who typo'd ``DEGUB`` would silently get INFO), an
    unrecognized name is reported to ``stderr`` so it stays discoverable.

    Args:
        name: A logging level name such as ``"DEBUG"`` or ``"WARNING"``.

    Returns:
        int: The numeric logging level, or ``logging.INFO`` if unrecognized.
    """
    level = getattr(logging, name.upper(), None)
    if isinstance(level, int):
        return level
    print(  # noqa: T201 - logging is not configured yet at this point
        f"Unknown log level {name!r}; falling back to INFO.", file=sys.stderr
    )
    return logging.INFO


def setup_logger() -> logging.Logger:
    """Set up and return the main logger for the project.

    Ensures that handlers are only added once to avoid duplicate log entries
    if this module is imported multiple times.

    Returns:
        logging.Logger: Configured logger for the project.
    """
    level = _resolve_level(get_settings().log_level)
    logger_ = logging.getLogger(PROJECT_NAME)
    logger_.setLevel(level)

    # Only add handlers if they haven't been added yet
    if not logger_.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Create a console handler for errors only. This is always available and
        # never depends on a writable filesystem.
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.ERROR)
        console_handler.setFormatter(formatter)
        logger_.addHandler(console_handler)

        # Add a rotating file handler when there is a user-owned directory to
        # write to. This runs at import time (loggers are created at module
        # load), so a read-only or unavailable ``$HOME`` -- locked-down
        # containers, service accounts, sandboxes -- must not crash read-only
        # commands like ``--help`` or ``version``. Degrade to console-only
        # logging instead, reporting it to ``stderr`` so it stays discoverable.
        if not HOME_IS_RESOLVABLE:
            # No home directory means no safe, user-private place for the log
            # file; falling back to a shared temp path would let another local
            # user hijack it, so skip file logging entirely.
            print(  # noqa: T201 - logging is only partially configured here
                "Home directory unavailable; using console-only logging.",
                file=sys.stderr,
            )
        else:
            try:
                ROOT_FOLDER_PATH.mkdir(parents=True, exist_ok=True)
                file_handler = RotatingFileHandler(
                    LOG_FILE_PATH, maxBytes=10 * 1024 * 1024, backupCount=5
                )
            except OSError as error:
                print(  # noqa: T201 - logging is only partially configured here
                    f"File logging unavailable ({error}); using console-only logging.",
                    file=sys.stderr,
                )
            else:
                file_handler.setLevel(level)
                file_handler.setFormatter(formatter)
                logger_.addHandler(file_handler)

    return logger_


@cache
def get_logger() -> logging.Logger:
    """Return the cached project logger.

    Returns:
        logging.Logger: The cached project logger.
    """
    return setup_logger()
