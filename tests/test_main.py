"""Tests for the package's runnable entrypoint (``python -m hwid``)."""

from __future__ import annotations

import importlib


def test_main_is_callable() -> None:
    """The package exposes a callable ``main()`` entrypoint.

    Every standalone-executable build (launcher / freezer / compiler)
    targets ``hwid.__main__:main``, so this pins the
    contract that the symbol exists and is callable for whichever component is
    enabled, and that the active branch's component import actually resolves.
    The module is imported (not executed as ``__main__``), so a runnable
    component's blocking ``main()`` (server loop, mainloop, ...) is never invoked.
    """
    main_module = importlib.import_module("hwid.__main__")

    assert callable(main_module.main)
    # The console root wires ``app`` into __main__; assert it resolved.
    assert hasattr(main_module, "app")
