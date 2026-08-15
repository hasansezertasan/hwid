"""CLI application for the project.

A dependency-free ``argparse`` root for the ``hwid`` command. It
exposes the same ``version`` / ``info`` commands as the Typer variant and hangs
every enabled non-primary component off the root as a lazily-imported subcommand
— ``hwid interactive`` (TUI), ``hwid web``, ... —
rather than a separate ``hwid-<name>`` console script (see
ADR-019 and ADR-020). Selected via ``cli_framework``.
"""

from __future__ import annotations

import argparse
import platform
import sys
from importlib.metadata import Distribution, PackageNotFoundError
from typing import TYPE_CHECKING, cast

from hwid.logger import logger

if TYPE_CHECKING:
    from collections.abc import Callable

__all__ = ["app", "info", "show_version"]

# The installed distribution name, used to resolve packaging metadata.
PROJECT_NAME = "hwid"

_METADATA_MISSING = f"Error: Package '{PROJECT_NAME}' metadata not found. Is the package installed correctly?"  # noqa: E501


def show_version() -> None:
    """Show the current version number of hwid.

    Show the version number:
        hwid version

    Example output:
        0.1.0

    Raises:
        SystemExit: With code 1 if the package metadata cannot be found.
    """
    try:
        distribution = Distribution.from_name(PROJECT_NAME)
    except PackageNotFoundError:
        # An uninstalled or partial package is an expected, user-facing error, so
        # log without the traceback that logging.exception would add.
        logger.error("Package metadata not found for %s", PROJECT_NAME)
        _ = sys.stderr.write(_METADATA_MISSING + "\n")
        raise SystemExit(1) from None
    logger.info("Command `version` called.")
    _ = sys.stdout.write(f"{distribution.version}\n")
    logger.info("Version displayed successfully.")


def info() -> None:
    """Display information about the hwid application.

    Show application information:
        hwid info

    Example output:
        Application Version: 0.1.0
        Python Version: 3.12.0 (CPython)
        Platform: Darwin

    Raises:
        SystemExit: With code 1 if the package metadata cannot be found.
    """
    try:
        distribution = Distribution.from_name(PROJECT_NAME)
    except PackageNotFoundError:
        # An uninstalled or partial package is an expected, user-facing error, so
        # log without the traceback that logging.exception would add.
        logger.error("Package metadata not found for %s", PROJECT_NAME)
        _ = sys.stderr.write(_METADATA_MISSING + "\n")
        raise SystemExit(1) from None
    logger.info("Command `info` called.")
    python_version = platform.python_version()
    python_implementation = platform.python_implementation()
    lines = [
        f"Application Version: {distribution.version}",
        f"Python Version: {python_version} ({python_implementation})",
        f"Platform: {platform.system()}",
    ]
    _ = sys.stdout.write("\n".join(lines) + "\n")
    logger.info("Application information displayed successfully.")


# Command name -> handler. ``version``/``info`` mirror the Typer root; a
# dispatcher is added for each enabled non-primary component.
_COMMANDS: dict[str, Callable[[], None]] = {"version": show_version, "info": info}


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser for the hwid CLI.

    Returns:
        The configured parser with the ``version``/``info`` commands and one
        subcommand per enabled non-primary component.
    """
    parser = argparse.ArgumentParser(prog="hwid")
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    _ = subparsers.add_parser("version", help="Show the version number.")
    _ = subparsers.add_parser("info", help="Show application and environment info.")
    return parser


def app(argv: list[str] | None = None) -> None:
    """Run the hwid CLI application.

    Args:
        argv: Optional argument vector; defaults to ``sys.argv[1:]`` when ``None``.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    # ``argparse.Namespace`` attributes are ``Any``; narrow the dispatch key.
    command = cast("str | None", args.command)
    handler = _COMMANDS.get(command) if command is not None else None
    if handler is None:
        # hwid's primary action: bare ``hwid`` prints the machine ID. The
        # ``version``/``info`` subcommands are dispatched above.
        from hwid.core import get_hwid  # noqa: PLC0415

        logger.info("Printing hardware ID.")
        _ = sys.stdout.write(f"HWID: {get_hwid()}\n")
        return
    handler()
