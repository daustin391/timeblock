""" Tests for Flask web interface

"""
# pylint: disable=redefined-outer-name
import subprocess
import time
from signal import SIGINT
import requests
import pytest
from pytest import main

URL = "http://127.0.0.1:5000/"


@pytest.fixture(scope="session", autouse=True)
def server():
    """Starts Flask dev server"""
    with subprocess.Popen(
        ["python", "/Users/daveaustin/programming/timeblock/timeblock/views.py"]
    ) as p:
        time.sleep(9)  # prevents requests before server runs
        yield
        p.send_signal(SIGINT)


def test_server():
    """Test that Flask server runs"""
    r = requests.get(URL)
    assert r.status_code == 200


if __name__ == "__main__":  # pragma: no cover
    main()
