"""Module entrypoint for the project.

This is the single runnable entrypoint used by ``python -m hwid`` and by every
standalone-executable build (PyCrucible launcher, PyInstaller freezer, Nuitka
compiler — see ADR-007). The build tools all target this file, so the launch
wiring lives here and nowhere else.

``main()`` runs the ``hwid`` CLI root, which prints the machine ID by default and
exposes ``version`` / ``info`` subcommands.
"""

from hwid.cli import app


def main() -> None:  # pragma: no cover
    """Run the hwid CLI root."""
    app()


__all__ = ["main"]


if __name__ == "__main__":
    main()
