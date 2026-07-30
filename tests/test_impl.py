"""Tests for the platform backends in :mod:`hwid.impl`.

``subprocess`` is mocked so every backend's parsing is exercised on any host OS.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from hwid.impl import darwin, linux, win32

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


def test_linux_strips_dmidecode_output(mocker: MockerFixture) -> None:
    """The linux backend returns the trimmed UUID from dmidecode."""
    check_output = mocker.patch(
        "hwid.impl.linux.subprocess.check_output", return_value=f"{VALID_HWID}\n"
    )

    assert linux.extract_hwid() == VALID_HWID
    assert check_output.call_args.kwargs == {"shell": True, "text": True}


def test_darwin_parses_system_profiler_line(mocker: MockerFixture) -> None:
    """The darwin backend extracts the value after the ``UUID:`` label."""
    line = f"          Hardware UUID: {VALID_HWID}\n"
    check_output = mocker.patch(
        "hwid.impl.darwin.subprocess.check_output", return_value=line
    )

    assert darwin.extract_hwid() == VALID_HWID
    assert check_output.call_args.kwargs == {"shell": True, "text": True}
