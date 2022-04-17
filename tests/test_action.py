""" Tests for Action class

"""
# pylint: disable=redefined-outer-name
from datetime import datetime, timedelta
from pytest import main, fixture
from timeblock.action import Action


apollo = datetime(1969, 7, 16, 13, 32)
to_orbit = timedelta(minutes=12)
retire = datetime(2011, 3, 9)
challenger_launch = datetime(1986, 1, 28, 16, 38)
til_explosion = timedelta(seconds=73)


@fixture
def instance():
    """Provides an instance of Action for testing"""
    return Action("test")


def test_repr(instance):
    """Test that __repr__ works"""
    assert instance.__repr__() == "Action('test')"


def test_start(instance):
    """Test that start date attr can be updated"""
    instance.start = apollo
    assert instance.start == apollo


def test_add_duration(instance):
    """Test that duration attr can be updated and endtime moves accordingly"""
    instance.start = apollo
    instance.est_duration = to_orbit
    assert instance.est_duration == to_orbit
    assert instance.end == datetime(1969, 7, 16, 13, 32 + 12)


def test_end(instance):
    """Test that end date attr can be updated and start date moves accordingly"""
    # end unset
    assert instance.end is None
    # end set through assignment, no duration
    instance.end = retire
    assert instance.end == retire
    # end set through assignment, with duration
    # start should move
    instance.est_duration = to_orbit
    instance.end = apollo
    assert instance.end == apollo
    assert instance.start == apollo - to_orbit


def test_change_duration(instance):
    """Test that duration attr can be updated and endtime moves accordingly"""
    instance.est_duration = to_orbit
    instance.start = challenger_launch
    instance.est_duration = til_explosion
    assert instance.end == challenger_launch + til_explosion


if __name__ == "__main__":  # pragma: no cover
    main()
