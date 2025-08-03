"""Core functionality for getting hardware IDs."""

# Copyright (c) 2023 Hasan Sezer Taşan
# Licensed under the MIT License

import re
from sys import platform

from hwid.exceptions import InvalidHWIDError, UnsupportedOSError
from hwid.impl import darwin, linux, win32


def validate_hwid(value: str) -> bool:
    """Validate if a string matches the HWID format.

    Args:
        value: The string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    return bool(
        re.match(r"^[a-fA-F0-9]{8}-([a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}$", value)
    )


def get_hwid() -> str:
    """Get the hardware ID of the current machine.

    Returns:
        str: The hardware ID string.

    Raises:
        UnsupportedOSError: If the operating system is not supported.
        InvalidHWIDError: If the retrieved hardware ID is invalid.
    """
    if platform in {"linux", "linux2"}:
        output = linux.extract_hwid()
    elif platform == "win32":
        output = win32.extract_hwid()
    elif platform == "darwin":
        output = darwin.extract_hwid()
    else:
        msg = "Unsupported OS"
        raise UnsupportedOSError(msg)

    if not validate_hwid(value=output):
        msg = "Invalid hardware ID"
        raise InvalidHWIDError(msg)

    return output
