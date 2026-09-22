"""Module entrypoint for the project.

<<<<<<< before updating
This is the single runnable entrypoint used by ``python -m hwid`` and by every
standalone-executable build (PyCrucible launcher, PyInstaller freezer, Nuitka
compiler — see ADR-007). The build tools all target this file, so the launch
wiring lives here and nowhere else.

``main()`` runs the ``hwid`` CLI root, which prints the machine ID by default and
exposes ``version`` / ``info`` subcommands.
=======
This is the single runnable entrypoint used by ``python -m hwid``
and by every standalone-executable build (PyCrucible launcher, PyInstaller
freezer, Nuitka compiler — see ADR-007). The build tools all target this file,
so the component-selection logic lives here and nowhere else.

When a ``hwid`` console root exists (``include_console_root`` —
the CLI, or ≥2 components sharing a launcher; see ADR-019), ``main()`` runs it,
which dispatches to the primary component by default and to each secondary via a
subcommand. Otherwise the single enabled component with the highest precedence —
CLI > GUI > TUI > web > MCP > worker — is wired to ``main()`` directly at
template-generation time (via the Jinja conditionals below). To change the
default entrypoint, re-render with a different component enabled or edit the
import/``main`` binding here directly. With no runnable component enabled,
``main()`` exits non-zero with an explanatory message.

Either binding routes its import through a loader that turns a missing
dependency into one actionable line instead of a traceback (ADR-028). This is
the boundary that needs it most: a standalone executable's user has no console
root to fall back on and no obvious way to read a Python stack trace.
>>>>>>> after updating
"""

from hwid.cli import app


def main() -> None:  # pragma: no cover
    """Run the hwid CLI root."""
    app()


__all__ = ["main"]


if __name__ == "__main__":
    main()
