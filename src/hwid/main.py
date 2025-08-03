"""Main module for the HWID package."""

# Copyright (c) 2023 Hasan Sezer Taşan
# Licensed under the MIT License

from hwid.core import get_hwid
from hwid.logger import logger


def app() -> None:
    """Get the HWID of the current machine."""
    msg = f"HWID: {get_hwid()}"
    logger.info(msg)
    print(msg)  # Print the HWID to standard output for visibility
