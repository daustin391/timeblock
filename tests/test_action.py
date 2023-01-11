"""
This module contains tests for the `Action` class.

Included are a set of date and time constants that are used as test data.
These constants are:
    - APOLLO: A datetime object (set to the launch of Apollo 11)
    - TO_ORBIT: A timedelta object (set to Apollo 11's time to Earth orbit)
    - RETIRE: A datetime object (set to the retirement of the Space Shuttle)
    - CHALLENGER: A datetime object (set to the launch of that Shuttle)
    - TO_EXPLOSION: A timedelta object (the duration of Challenger's flight)

This fixture is imported from tests/conftest.py:
    - instance: An instance of Action with Action.desc set to "test".

The tests cover the following:
    - The `__repr__` method returns a string representation of the object.
    - The `start` property can be updated.
    - The `end` property can be updated.
    - The `est_duration` attribute can be updated.
    - The alternate constructor `from_tuple` can create an Action object.
"""

from datetime import datetime, timedelta

from timeblock.action import Action


APOLLO = datetime(1969, 7, 16, 13, 32)
TO_ORBIT = timedelta(minutes=12)
RETIRE = datetime(2011, 3, 9)
CHALLENGER = datetime(1986, 1, 28, 16, 38)
TO_EXPLOSION = timedelta(seconds=73)


def test_repr(instance: Action):
    """
    Test that __repr__ returns a string representation of the object.

    Args:
        instance (Action): An instance of Action with Action.desc set to "test"
    """
    assert repr(instance) == "Action('test')"


def test_start(instance: Action):
    """
    Test that the 'start' property can be updated.

    This test sets 'start' to a specific value and verifies that
    the getter method returns the correct value.

    It also tests the behavior when 'end' and 'est_duration' are set.
    If these are set and 'start' is not, 'start' should be set
    to 'end' minus 'est_duration'.

    Args:
        instance (Action): An instance of Action with Action.desc set to "test"
    """
    assert instance.start is None
    instance.start = APOLLO
    assert instance.start == APOLLO

    instance.est_duration = TO_ORBIT
    instance.end = APOLLO
    assert instance.start == APOLLO - TO_ORBIT


def test_end(instance: Action):
    """
    Test that the 'end' property can be updated.

    This test sets 'end' to a specific value and verifies that
    the getter method returns the correct value.

    It also tests the behavior when 'start' and 'est_duration' is set.
    If these are set, 'end' should be set to 'start' plus 'est_duration'.

    Args:
        instance (Action): An instance of Action with Action.desc set to "test"
    """
    assert instance.end is None
    instance.end = RETIRE
    assert instance.end == RETIRE

    instance.start = CHALLENGER
    instance.est_duration = TO_EXPLOSION
    assert instance.end == CHALLENGER + TO_EXPLOSION


def test_add_duration(instance: Action):
    """
    Test that the 'est_duration' attribute can be updated.

    Args:
        instance (Action): An instance of Action with Action.desc set to "test"
    """
    assert instance.est_duration is None
    instance.est_duration = TO_ORBIT
    assert instance.est_duration == TO_ORBIT


def test_change_duration(instance: Action):
    """
    Test that the 'est_duration' attribute can be changed.

    Checks how changing 'est_duration' affects 'start' and 'end'.
    Changing 'est_duration' should move 'end' if 'start' is set.

    Args:
        instance (Action): An instance of Action with Action.desc set to "test"
    """
    assert instance.est_duration is None
    instance.est_duration = TO_ORBIT
    instance.start = CHALLENGER
    assert instance.end == CHALLENGER + TO_ORBIT
    instance.est_duration = TO_EXPLOSION
    assert instance.end == CHALLENGER + TO_EXPLOSION


def test_from_tuple():
    """Test that 'from_tuple' constructor creates the correct 'Action'."""
    fixture_action = Action.from_tuple((1, "test", 1500, None, None))
    assert fixture_action.desc == "test"
    assert fixture_action.est_duration == timedelta(minutes=25)
