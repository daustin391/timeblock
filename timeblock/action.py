""" Action object
    A class for representing and manipulating blocks of time
"""
from datetime import timedelta, datetime
from typing import Optional


class Action:
    """A representation of actions, events, etc. in time
    and methods for manipulating them"""

    def __init__(
        self,
        desc: str,
        est_duration: Optional[timedelta] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ):
        self.actual_duration: Optional[timedelta] = None
        self.desc = desc
        self.est_duration = est_duration
        self._start = start
        self._end = end

    def __repr__(self):
        return f"Action('{self.desc}')"

    @property
    def start(self):
        """The time an action is scheduled to take place"""
        return self._start

    @start.setter
    def start(self, value: datetime):
        self._start = value

    @property
    def end(self):
        """The time an action is expected to end"""
        if self._start:
            return self.start + self.est_duration
        return self._end

    @end.setter
    def end(self, value: datetime):
        if self.est_duration:
            self._start = value - self.est_duration
        else:
            self._end = value
