"""Core functionality for getting hardware IDs."""

# Copyright (c) 2023 Hasan Sezer Taşan
# Licensed under the MIT License

import re
import subprocess
from sys import platform

from hwid.exceptions import InvalidHWIDError, UnsupportedOSError


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
        command = "sudo dmidecode -s system-uuid"
        output = subprocess.check_output(command, shell=True)
        output = output.decode("utf-8").strip()
    elif platform == "win32":
        command = 'powershell -Command "(Get-CimInstance -ClassName Win32_ComputerSystemProduct).UUID"'
        output = subprocess.check_output(command, shell=True)
        output = output.decode("utf-8").strip()
    elif platform == "darwin":
        command = "system_profiler SPHardwareDataType | grep 'UUID'"
        output = subprocess.check_output(command, shell=True)
        output = output.decode("utf-8").strip()
        output = output.split(":")[1].strip()
    else:
        msg = "Unsupported OS"
        raise UnsupportedOSError(msg)
    if validate_hwid(value=output):
        return output
    msg = "Invalid HWID"
    raise InvalidHWIDError(msg)
