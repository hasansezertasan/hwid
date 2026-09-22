"""Tests for the shared application payload every component adapts over."""

from __future__ import annotations

import platform
from importlib.metadata import Distribution

import pytest

from hwid.__metadata__ import PROJECT_NAME
from hwid.core import app as service


def test_version_matches_the_installed_distribution() -> None:
    """``version()`` reports the installed distribution's version."""
    assert service.version() == Distribution.from_name(PROJECT_NAME).version


def test_info_carries_the_version_and_the_runtime_environment() -> None:
    """``info()`` is the payload every interface renders, in one shape.

    Given:
        - An installed package.
    When:
        - The shared payload is built.
    Then:
        - It carries exactly the four keys the components format, filled from
          the distribution metadata and the running interpreter.
    """
    payload = service.info()

    assert set(payload) == {
        "application_version",
        "platform",
        "python_implementation",
        "python_version",
    }
    assert payload["application_version"] == service.version()
    assert payload["python_version"] == platform.python_version()
    assert payload["python_implementation"] == platform.python_implementation()
    assert payload["platform"] == platform.system()


@pytest.mark.usefixtures("missing_metadata")
def test_version_raises_when_metadata_is_unreadable() -> None:
    """A broken install raises the service's own error, not importlib's.

    Given:
        - Package metadata that cannot be resolved.
    When:
        - The version is requested.
    Then:
        - ``MetadataUnavailableError`` names the package and suggests a check,
          so no component has to interpret ``PackageNotFoundError`` itself.
    """
    with pytest.raises(service.MetadataUnavailableError) as excinfo:
        _ = service.version()

    assert PROJECT_NAME in str(excinfo.value)


@pytest.mark.usefixtures("missing_metadata")
def test_info_propagates_the_metadata_failure() -> None:
    """``info()`` fails the same way, so a transport can map it to its own error."""
    with pytest.raises(service.MetadataUnavailableError):
        _ = service.info()


@pytest.mark.usefixtures("missing_metadata")
def test_info_or_unknown_degrades_instead_of_raising() -> None:
    """The degrading variant keeps the payload usable for a GUI or TUI panel.

    Given:
        - Package metadata that cannot be resolved.
    When:
        - The degrading payload is built.
    Then:
        - Only the version is replaced; the environment fields are still real,
          which is what makes an "unknown" panel worth showing at all.
    """
    payload = service.info_or_unknown()

    assert payload["application_version"] == service.UNKNOWN_VERSION
    assert payload["platform"] == platform.system()


def test_info_or_unknown_reports_the_real_version_when_available() -> None:
    """With metadata present the degrading variant is just ``info()``."""
    assert service.info_or_unknown() == service.info()
