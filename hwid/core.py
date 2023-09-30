import subprocess
from sys import platform
import re
from .exceptions import UnsupportedOS, InvalidHWID

def validate_hwid(hwid):
    if re.match(r"^[a-fA-F0-9]{8}-([a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}$", hwid):
        return True
    else:
        return False

def get_hwid():
    """Gets the HWID."""
    if platform in ["linux", "linux2"]:
        command = "sudo dmidecode -s system-uuid"
        output = subprocess.check_output(command, shell=True)
        output = output.decode("utf-8").strip()
    elif platform in ["win32"]:
        command = "wmic csproduct get uuid"
        output = subprocess.check_output(command, shell=True)
        output = output.decode("utf-8").strip()
        output = output.split("\n")[1].strip()
    elif platform in ["darwin"]:
        command = "system_profiler SPHardwareDataType | grep 'UUID'"
        output = subprocess.check_output(command, shell=True)
        output = output.decode("utf-8").strip()
        output = output.split(":")[1].strip()
    else:
        raise UnsupportedOS("Unsupported OS")
    if validate_hwid(output):
        return output
    else:
        raise InvalidHWID("Invalid HWID")
