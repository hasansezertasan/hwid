import re
import subprocess
from sys import platform

from hwid.exceptions import InvalidHWIDError, UnsupportedOSError


def validate_hwid(hwid) -> bool:
    return bool(re.match(r"^[a-fA-F0-9]{8}-([a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}$", hwid))


def get_hwid():
    """Gets the HWID."""
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
    if validate_hwid(output):
        return output
    msg = "Invalid HWID"
    raise InvalidHWIDError(msg)
