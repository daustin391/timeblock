"""Define Action class for representing and manipulating blocks of time."""
from datetime import timedelta, datetime
from typing import Optional


class Action:
    """
    A block of time.

    Constructors:
        Action()
        from_tuple()

    Properties:
        start
        end

    Attributes:
        desc
        est_duration
        actual_duration
    """

    def __init__(
        self,
        desc: str,
        est_duration: Optional[timedelta] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ):
        """
        Instantiate Action object.

        Args:
            desc: A string describing the action.

            Optionally, datetimes can be passed to set start and end,
            or a timedelta can be passed to set est_duration.
        """
        self.actual_duration: Optional[timedelta] = None
        self.desc = desc
        self.est_duration = est_duration
        self._start = start
        self._end = end

    def __repr__(self):
        """Return string resembling constructor call."""
        return f"Action('{self.desc}')"

    @property
    def start(self):
        """Access the datetime the action started or is scheduled to start."""
        return self._start

    @start.setter
    def start(self, value: datetime):
        self._start = value

    @property
    def end(self):
        """Access the datetime the action ended or is expected to end."""
        if self._start:
            return self.start + self.est_duration
        return self._end

    @end.setter
    def end(self, value: datetime):
        if self.est_duration:
            self._start = value - self.est_duration
        else:
            self._end = value

    @classmethod
    def from_tuple(cls, action: tuple) -> "Action":
        """
        Construct Action from a tuple.

        The tuple should be the same format as returned by the SQL query:
        "SELECT * FROM action"
        (id, description, estimated_duration, actual_duration, start_datetime)

        Args:
            action
        """
        est_duration = timedelta(seconds=action[2]) if action[2] else None
        return cls(action[1], est_duration=est_duration)
