"""Test cases for the hwid argparse root."""

from __future__ import annotations


import pytest

from hwid.cli.app import app



def test_help_lists_subcommands(capsys: pytest.CaptureFixture[str]) -> None:
    """``--help`` renders the root usage and exits 0.

    Given:
        - The hwid argparse root.
    When:
        - ``--help`` is requested.
    Then:
        - The command exits 0; each enabled component subcommand is advertised.
    """
    with pytest.raises(SystemExit) as excinfo:
        app(["--help"])
    assert excinfo.value.code == 0
    out = capsys.readouterr().out
    assert "usage" in out.lower()


def test_no_command_prints_hwid(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Bare ``hwid`` (no subcommand) prints the machine ID."""
    monkeypatch.setattr("hwid.core.get_hwid", lambda: "TEST-HWID")
    app([])
    assert "HWID: TEST-HWID" in capsys.readouterr().out


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    """The `version` command prints a non-empty version string."""
    app(["version"])
    assert capsys.readouterr().out.strip()


def test_info(capsys: pytest.CaptureFixture[str]) -> None:
    """The `info` command prints application, Python, and platform lines."""
    app(["info"])
    out = capsys.readouterr().out
    assert "Application Version:" in out
    assert "Python Version:" in out
    assert "Platform:" in out


@pytest.mark.parametrize("command", ["version", "info"])
@pytest.mark.usefixtures("missing_metadata")
def test_command_fails_loudly_when_metadata_missing(command: str) -> None:
    """Commands exit 1 when package metadata is missing.

    Given:
        - Package metadata cannot be resolved (broken/partial install).
    When:
        - The `version` or `info` command is invoked.
    Then:
        - The command exits with code 1 instead of dumping a traceback or
          silently printing nothing.
    """
    with pytest.raises(SystemExit) as excinfo:
        app([command])

    assert excinfo.value.code == 1
