"""Tests for the logging setup module."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from typing import TYPE_CHECKING

import pytest

from hwid.__metadata__ import PROJECT_NAME
from hwid.core import logging_setup
from hwid.core.logging_setup import _resolve_level, setup_logger

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("DEBUG", logging.DEBUG),
        ("info", logging.INFO),
        ("Warning", logging.WARNING),
        ("ERROR", logging.ERROR),
        ("CRITICAL", logging.CRITICAL),
    ],
)
def test_resolve_level_known(name: str, expected: int) -> None:
    """Known level names resolve to their numeric value, case-insensitively."""
    assert _resolve_level(name) == expected


def test_resolve_level_unknown_falls_back_to_info(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An unknown level falls back to INFO and reports it to stderr."""
    assert _resolve_level("DEGUB") == logging.INFO

    captured = capsys.readouterr()
    assert "DEGUB" in captured.err


def test_setup_logger_returns_configured_project_logger() -> None:
    """``setup_logger`` returns the project logger with handlers attached."""
    configured = setup_logger()

    assert configured.name == PROJECT_NAME
    # A file handler and a console handler are wired up.
    assert configured.handlers


def test_setup_logger_is_idempotent() -> None:
    """Repeated calls reuse the same logger without duplicating handlers."""
    first = setup_logger()
    handler_count = len(first.handlers)

    second = setup_logger()

    assert second is first
    assert len(second.handlers) == handler_count


@pytest.fixture
def isolated_project_logger() -> Iterator[logging.Logger]:
    """Yield the project logger with its handlers isolated for one test.

    Detaches (without closing) the shared logger's existing handlers so
    ``setup_logger`` re-adds them under the test, then restores them: handlers
    created during a degradation test are bound to ``capsys``'s transient
    ``stderr``, which pytest closes at teardown, so leaving them attached would
    break error logging in later tests.

    Yields:
        logging.Logger: The project logger with its handlers detached.
    """
    logger_ = logging.getLogger(PROJECT_NAME)
    original_handlers = logger_.handlers[:]
    for handler in original_handlers:
        logger_.removeHandler(handler)
    try:
        yield logger_
    finally:
        for handler in logger_.handlers[:]:
            logger_.removeHandler(handler)
            handler.close()
        for handler in original_handlers:
            logger_.addHandler(handler)


def test_setup_logger_degrades_when_log_dir_unavailable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    isolated_project_logger: logging.Logger,
) -> None:
    """A read-only log directory degrades to console-only logging without raising."""
    # Point the log directory below a regular file so ``mkdir`` raises a real
    # ``NotADirectoryError`` (an ``OSError``), standing in for a read-only
    # ``$HOME`` cross-platform.
    blocker = tmp_path / "blocker"
    blocker.write_text("not a directory")
    monkeypatch.setattr(logging_setup, "ROOT_FOLDER_PATH", blocker / "logs")

    configured = setup_logger()

    # Console logging survives on the isolated logger; no file handler attached.
    assert configured is isolated_project_logger
    assert configured.handlers
    assert not any(
        isinstance(handler, RotatingFileHandler) for handler in configured.handlers
    )
    # The degradation is reported to stderr so it stays discoverable.
    assert "console-only" in capsys.readouterr().err


def test_setup_logger_skips_file_logging_without_home(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    isolated_project_logger: logging.Logger,
) -> None:
    """An unresolvable home directory uses console-only logging, never a file."""
    monkeypatch.setattr(logging_setup, "HOME_IS_RESOLVABLE", False)
    # Point at a writable directory: if file logging were attempted it would
    # succeed and create it, so asserting it stays absent proves the guard
    # skipped file logging rather than merely failing to write.
    log_dir = tmp_path / "logs"
    monkeypatch.setattr(logging_setup, "ROOT_FOLDER_PATH", log_dir)

    configured = setup_logger()

    assert configured is isolated_project_logger
    assert not log_dir.exists()
    assert configured.handlers
    assert not any(
        isinstance(handler, RotatingFileHandler) for handler in configured.handlers
    )
    assert "console-only" in capsys.readouterr().err
