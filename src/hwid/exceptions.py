"""Exceptions for the HWID package."""

# Copyright (c) 2023 Hasan Sezer Taşan
# Licensed under the MIT License


class UnsupportedOSError(Exception):
    """Raised when the operating system is not supported."""


class InvalidHWIDError(Exception):
    """Raised when the hardware ID is invalid."""
