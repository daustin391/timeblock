""" Tests for Stopwatch module

"""

from datetime import timedelta
from pytest import main
from timeblock.stopwatch import Stopwatch


def test_start():
    """Test that the Stopwatch can be started and return timedelta"""
    watch = Stopwatch()
    watch.start()
    assert isinstance(watch.check(), timedelta)


if __name__ == "__main__":
    main()
