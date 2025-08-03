"""`win32` implementation for getting hardware IDs."""

# Copyright (c) 2023 Hasan Sezer Taşan
# Licensed under the MIT License
import subprocess


def extract_hwid() -> str:
    """Extract the hardware ID from the output string.

    Returns:
        str: The extracted hardware ID.
    """
    command = 'powershell -Command "(Get-CimInstance -ClassName Win32_ComputerSystemProduct).UUID"'  # noqa: E501
    output = subprocess.check_output(command, shell=True, text=True)
    return output.strip()
