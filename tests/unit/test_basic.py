"""Basic test module for the content optimizer."""

from optimizer import __version__


def test_basic() -> None:
    """Basic test to ensure pytest is working."""
    assert True


def test_version() -> None:
    """Test that version is properly set."""
    assert isinstance(__version__, str)
    assert len(__version__.split('.')) == 3 