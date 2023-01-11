"""
Tests for `Stopwatch` class.

The test covers the following:
    - Start the Stopwatch and check that it returns a timedelta.
"""

from datetime import timedelta
from timeblock.stopwatch import Stopwatch


def test_start():
    """Start a Stopwatch object and test that .check() returns a timedelta."""
    watch = Stopwatch()
    watch.start()
    assert isinstance(watch.check(), timedelta)
