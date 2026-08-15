"""Tests for :mod:`hwid.core.impl.darwin`; ``subprocess`` is mocked on any host."""

from __future__ import annotations

from typing import TYPE_CHECKING

from hwid.core.impl import darwin

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

VALID_HWID = "D486629F-0026-55CC-988A-C086D16715C1"


def test_darwin_parses_system_profiler_line(mocker: MockerFixture) -> None:
    """The darwin backend extracts the value after the ``UUID:`` label."""
    line = f"          Hardware UUID: {VALID_HWID}\n"
    check_output = mocker.patch(
        "hwid.core.impl.darwin.subprocess.check_output", return_value=line
    )

    assert darwin.extract_hwid() == VALID_HWID
    check_output.assert_called_once()
    assert check_output.call_args.args == (
        "system_profiler SPHardwareDataType | grep 'UUID'",
    )
    assert check_output.call_args.kwargs == {"shell": True, "text": True}


def test_darwin_returns_empty_on_missing_delimiter(mocker: MockerFixture) -> None:
    """Profiler output without a ``:`` yields ``""`` rather than an ``IndexError``."""
    mocker.patch(
        "hwid.core.impl.darwin.subprocess.check_output", return_value="no uuid here\n"
    )

    assert not darwin.extract_hwid()
