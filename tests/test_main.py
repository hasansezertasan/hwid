"""Tests for the CLI entrypoint in :mod:`hwid.main` and ``python -m hwid``."""

from __future__ import annotations

import importlib
import logging
from typing import TYPE_CHECKING

from hwid.main import app

if TYPE_CHECKING:
    import pytest
    from pytest_mock import MockerFixture

VALID_HWID = "D486629F-0026-55CC-988A-C086D16715C1"


def test_app_prints_and_logs_hwid(
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """``app`` writes ``HWID: <value>`` to stdout and logs it at INFO."""
    mocker.patch("hwid.main.get_hwid", return_value=VALID_HWID)

    with caplog.at_level(logging.INFO, logger="hwid.logger"):
        app()

    assert capsys.readouterr().out.strip() == f"HWID: {VALID_HWID}"
    assert f"HWID: {VALID_HWID}" in caplog.text


def test_dunder_main_exposes_app() -> None:
    """``python -m hwid`` resolves ``app`` via the ``__main__`` module."""
    module = importlib.import_module("hwid.__main__")

    assert module.app is app
