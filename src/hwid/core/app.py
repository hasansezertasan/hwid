"""The application payload every interface component renders.

The CLI command, the web endpoint, the MCP tool, the GUI/TUI panel and the
worker handler all answer the same two questions — what version is this, and
what is it running on. This module answers them once; each component is an
*adapter* that decides only how to transport and present the answer, and how to
report the one failure mode (unreadable package metadata) in its own terms:
the CLI exits 1, the web app answers 503, the GUI degrades to "unknown".

Adding a component therefore means writing an adapter, not another copy of the
metadata lookup. See ADR-033.

It lives in ``core`` — already the layer directly beneath the independent
component group in the import-linter contract (ADR-014) — so every component
may import it and none may import another.
"""

from __future__ import annotations

import platform
from importlib.metadata import Distribution, PackageNotFoundError

from hwid.__metadata__ import PROJECT_NAME
from hwid.core.logging_setup import get_logger

__all__ = [
    "UNKNOWN_VERSION",
    "MetadataUnavailableError",
    "info",
    "info_or_unknown",
    "version",
]

logger = get_logger()

#: Stand-in used by the interfaces that degrade rather than fail when the
#: package metadata is unreadable (the GUI and TUI panels).
UNKNOWN_VERSION = "unknown"

_METADATA_MISSING = (
    f"Package '{PROJECT_NAME}' metadata not found. Is the package installed correctly?"
)


class MetadataUnavailableError(RuntimeError):
    """Raised when the installed package metadata cannot be read.

    Means the package is not installed, or only partially so. Each component
    maps it onto its own transport's failure rather than letting an
    ``importlib.metadata`` exception leak into an HTTP response or a tool
    result.
    """


def version() -> str:
    """Return the installed version of hwid.

    Returns:
        str: The version string from the installed distribution metadata.

    Raises:
        MetadataUnavailableError: If the distribution metadata cannot be read.
    """
    try:
        distribution = Distribution.from_name(PROJECT_NAME)
    except PackageNotFoundError as exc:
        raise MetadataUnavailableError(_METADATA_MISSING) from exc
    return distribution.version


def info() -> dict[str, str]:
    """Return the application version plus the runtime environment.

    Propagates ``MetadataUnavailableError`` from ``version()`` when the
    distribution metadata cannot be read.

    Returns:
        dict[str, str]: ``application_version``, ``python_version``,
            ``python_implementation`` and ``platform``.
    """
    return _payload(version())


def info_or_unknown() -> dict[str, str]:
    """Return the same payload, degrading the version instead of raising.

    For the interfaces that should still show *something* when the metadata is
    unreadable: a GUI dialog or TUI panel reporting "unknown" is more useful
    than one that fails to open.

    Returns:
        dict[str, str]: As ``info()``, with ``application_version`` set to
            ``UNKNOWN_VERSION`` when the metadata is unavailable.
    """
    try:
        resolved = version()
    except MetadataUnavailableError:
        # Expected on a partial install, and already degraded here, so log
        # without the traceback that logging.exception would add.
        logger.warning("Package metadata not found for %s", PROJECT_NAME)
        resolved = UNKNOWN_VERSION
    return _payload(resolved)


def _payload(resolved_version: str) -> dict[str, str]:
    """Build the info payload around an already-resolved version.

    Args:
        resolved_version: The version string to report.

    Returns:
        dict[str, str]: The full payload.
    """
    return {
        "application_version": resolved_version,
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.system(),
    }
