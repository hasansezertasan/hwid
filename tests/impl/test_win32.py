"""Tests for :mod:`hwid.impl.win32`. ``subprocess`` is mocked to run on any host."""

from __future__ import annotations

from typing import TYPE_CHECKING

from hwid.impl import win32

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

VALID_HWID = "D486629F-0026-55CC-988A-C086D16715C1"


def test_win32_strips_powershell_output(mocker: MockerFixture) -> None:
    """The win32 backend returns the trimmed UUID from PowerShell."""
    check_output = mocker.patch(
        "hwid.impl.win32.subprocess.check_output", return_value=f"{VALID_HWID}\r\n"
    )

    assert win32.extract_hwid() == VALID_HWID
    check_output.assert_called_once()
    assert check_output.call_args.kwargs == {"shell": True, "text": True}
