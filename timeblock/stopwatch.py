"""
A Stopwatch class for measuring elapsed time.

Example:
>>> from timeblock import stopwatch
>>> watch = stopwatch.Stopwatch()
>>> watch.start()
>>> # Two minutes later...
>>> watch.check()
datetime.timedelta(seconds=120)
"""
from datetime import datetime, timedelta


class Stopwatch:
    """
    Stopwatch object for measuring time.

    Methods:
        start(): Starts watch by setting start time to now.
        check() -> timedelta: Check the time passed since watch started
    """

    def __init__(self):
        """Initialize Stopwatch object."""
        self._start = None

    def start(self: "Stopwatch") -> None:
        """Start watch by recording the current time."""
        self._start = datetime.now()

    def check(self: "Stopwatch") -> timedelta:
        """Return timedelta of time passed since watch started."""
        return self._start - datetime.now()
