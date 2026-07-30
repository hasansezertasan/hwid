"""Smoke tests for hwid package."""


def test_smoke() -> None:
    """Test that the package can be imported."""
    import hwid  # noqa: PLC0415

    assert hwid is not None
