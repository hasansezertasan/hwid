"""Tests for :mod:`hwid.core.impl.linux`; ``subprocess`` is mocked on any host."""

from __future__ import annotations

from typing import TYPE_CHECKING

from hwid.core.impl import linux

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

VALID_HWID = "D486629F-0026-55CC-988A-C086D16715C1"


def test_linux_strips_dmidecode_output(mocker: MockerFixture) -> None:
    """The linux backend returns the trimmed UUID from dmidecode."""
    check_output = mocker.patch(
        "hwid.core.impl.linux.subprocess.check_output", return_value=f"{VALID_HWID}\n"
    )

    assert linux.extract_hwid() == VALID_HWID
    check_output.assert_called_once()
    assert check_output.call_args.args == ("sudo dmidecode -s system-uuid",)
    assert check_output.call_args.kwargs == {"shell": True, "text": True}
