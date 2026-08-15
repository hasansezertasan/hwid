"""This module is the entry point of the application."""

<<<<<<< before updating
# Copyright (c) 2023 Hasan Sezer Taşan
# Licensed under the MIT License
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
"""

import sys


def main() -> None:
    """Fail loudly: no runnable application component is enabled.

    A standalone-executable build was produced for a project with no
    CLI/GUI/TUI/web/MCP/worker component, so there is nothing to run. Exit with
    a non-zero status and a message rather than a silent no-op, which would look
    like a broken binary to whoever launched it.
    """
    sys.exit("No runnable application component is enabled; nothing to run.")


__all__ = ["main"]
>>>>>>> after updating

from hwid.main import app

if __name__ == "__main__":
    app()
