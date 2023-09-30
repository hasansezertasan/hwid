from .core import get_hwid


def app():
    """
    Get the HWID of the current machine.
    """
    hwid = get_hwid()
    print(f"HWID: {hwid}")
