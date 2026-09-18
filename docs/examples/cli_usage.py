"""CLI argument parsing."""

from __future__ import annotations

from typing import TYPE_CHECKING

from hwid.cli.app import build_parser

if TYPE_CHECKING:
    import argparse


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse CLI arguments without executing a command.

    Args:
        argv: Argument vector to parse.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    return build_parser().parse_args(argv)
