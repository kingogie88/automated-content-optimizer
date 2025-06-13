"""Basic test module for the content optimizer."""

from typing import Any, cast

from optimizer import __version__


def test_basic() -> None:
    """Basic test to ensure pytest is working."""
    assert True


def test_version() -> None:
    """Test that version is properly set."""
    version: str = cast(str, __version__)
    assert isinstance(version, str)
    assert len(version.split('.')) == 3 