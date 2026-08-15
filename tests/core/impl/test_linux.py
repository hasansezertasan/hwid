"""Tests for :mod:`hwid.core.impl.linux`; ``subprocess`` is mocked on any host."""

from __future__ import annotations

import subprocess  # noqa: S404
from typing import TYPE_CHECKING

import pytest

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
    # argv (no shell) so the timeout kills sudo directly; `-n` stays non-interactive.
    assert check_output.call_args.args == (
        ["sudo", "-n", "dmidecode", "-s", "system-uuid"],
    )
    assert check_output.call_args.kwargs == {
        "text": True,
        "timeout": linux.COMMAND_TIMEOUT,
    }


@pytest.mark.parametrize(
    "error",
    [
        subprocess.CalledProcessError(1, "sudo"),
        subprocess.TimeoutExpired("sudo", 5),
        FileNotFoundError(2, "No such file or directory", "sudo"),
    ],
)
def test_linux_returns_empty_on_subprocess_failure(
    mocker: MockerFixture, error: Exception
) -> None:
    """A sudo denial, timeout, or missing sudo/dmidecode yields ``""`` (invalid)."""
    mocker.patch("hwid.core.impl.linux.subprocess.check_output", side_effect=error)

    assert not linux.extract_hwid()
