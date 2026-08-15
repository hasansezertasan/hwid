"""Tests for :mod:`hwid.core.resolution` -- validation and platform dispatch."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from hwid.core.exceptions import InvalidHWIDError, UnsupportedOSError
from hwid.core.resolution import get_hwid, validate_hwid

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

VALID_HWID = "D486629F-0026-55CC-988A-C086D16715C1"


@pytest.mark.parametrize(
    "value",
    [
        VALID_HWID,
        "00000000-0000-0000-0000-000000000000",
        "abcdef12-3456-7890-abcd-ef1234567890",
    ],
)
def test_validate_hwid_accepts_uuid_format(value: str) -> None:
    """A canonical 8-4-4-4-12 hex UUID validates as True."""
    assert validate_hwid(value) is True


@pytest.mark.parametrize(
    "value",
    [
        "",
        "not-a-hwid",
        "D486629F-0026-55CC-988A",  # too short
        "G486629F-0026-55CC-988A-C086D16715C1",  # non-hex char
        "D486629F0026-55CC-988A-C086D16715C1",  # missing separator
    ],
)
def test_validate_hwid_rejects_bad_input(value: str) -> None:
    """Anything that is not the exact UUID format validates as False."""
    assert validate_hwid(value) is False


@pytest.mark.parametrize(
    ("plat", "backend"),
    [("linux", "linux"), ("linux2", "linux"), ("win32", "win32"), ("darwin", "darwin")],
)
def test_get_hwid_dispatches_per_platform(
    mocker: MockerFixture, plat: str, backend: str
) -> None:
    """``get_hwid`` routes to the backend matching ``sys.platform``."""
    mocker.patch("hwid.core.resolution.platform", plat)
    extractor = mocker.patch(
        f"hwid.core.resolution.{backend}.extract_hwid", return_value=VALID_HWID
    )

    assert get_hwid() == VALID_HWID
    extractor.assert_called_once_with()


def test_get_hwid_raises_on_unsupported_os(mocker: MockerFixture) -> None:
    """An unknown platform raises :class:`UnsupportedOSError`."""
    mocker.patch("hwid.core.resolution.platform", "sunos5")

    with pytest.raises(UnsupportedOSError):
        get_hwid()


def test_get_hwid_raises_on_malformed_backend_output(mocker: MockerFixture) -> None:
    """A backend returning a non-UUID string raises :class:`InvalidHWIDError`."""
    mocker.patch("hwid.core.resolution.platform", "darwin")
    mocker.patch("hwid.core.resolution.darwin.extract_hwid", return_value="garbage")

    with pytest.raises(InvalidHWIDError):
        get_hwid()
