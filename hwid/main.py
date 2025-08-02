from hwid.core import get_hwid


def app() -> None:
    """Get the HWID of the current machine."""
    get_hwid()
