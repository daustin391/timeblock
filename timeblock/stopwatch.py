""" Stopwatch
    A simple stopwatch for measuring time
"""
from datetime import datetime


class Stopwatch:
    """Stopwatch object for measuring time"""

    def __init__(self):
        self._start = None

    def start(self):
        """Starts watch by setting start time to now"""
        self._start = datetime.now()

    def check(self):
        """Check the time passed since watch started"""
        return self._start - datetime.now()
