"""`linux` implementation for getting hardware IDs."""

# Copyright (c) 2023 Hasan Sezer Taşan
# Licensed under the MIT License
import subprocess

__all__ = ["extract_hwid"]

# Bound the dmidecode call so HWID resolution can never hang.
COMMAND_TIMEOUT = 5


def extract_hwid() -> str:
    """Extract the hardware ID from the output string.

    Returns:
        str: The extracted hardware ID, or "" if it cannot be read.
    """
    # Run without a shell so the timeout kills ``sudo`` directly instead of an
    # intermediate ``/bin/sh`` that could orphan privileged descendants.
    # ``sudo -n`` keeps this non-interactive: without cached credentials it fails
    # fast instead of blocking on a password prompt. A denial, timeout, or a
    # missing ``sudo``/``dmidecode`` returns "" so ``get_hwid`` raises
    # ``InvalidHWIDError`` via validation rather than leaking a raw traceback.
    command = ["sudo", "-n", "dmidecode", "-s", "system-uuid"]
    try:
        output = subprocess.check_output(command, text=True, timeout=COMMAND_TIMEOUT)
    except (subprocess.SubprocessError, OSError):
        return ""
    return output.strip()
