"""Look up the version of the installed distribution."""

from importlib.metadata import version

from hwid.__metadata__ import PROJECT_NAME


def version_lookup() -> str:
    """Return the installed distribution version for this project.

    Returns:
        str: The installed distribution version.
    """
    return version(PROJECT_NAME)
