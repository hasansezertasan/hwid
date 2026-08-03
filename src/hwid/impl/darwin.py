"""`darwin` implementation for getting hardware IDs."""

# Copyright (c) 2023 Hasan Sezer Taşan
# Licensed under the MIT License
import subprocess

__all__ = ["extract_hwid"]


def extract_hwid() -> str:
    """Extract the hardware ID from the output string.

    Returns:
        str: The extracted hardware ID.
    """
    command = "system_profiler SPHardwareDataType | grep 'UUID'"
    output = subprocess.check_output(command, shell=True, text=True)
    output = output.strip()
    return output.split(":")[1].strip()
