"""
This module contains tests for the Timeblock application.

These constants are imported from the constants.py module:
    - TEST_DB_PATH: The path to the test database.
    - URL: The URL of the Flask server.

This module is using fixtures from the conftest.py module:
    - app: Runs the application and Flask server for testing.
    - tb_db: An empty TimeblockDB instance.

The tests cover the following:
    - POST requests add an action to the database.
"""

import requests
import pytest

from constants import URL
from timeblock import sql


@pytest.mark.usefixtures("app")
def test_post_request(tb_db: sql.TimeblockDB) -> None:
    """
    Test that POST requests add an action to the database.

    This test checks that a POST request to '/' adds an action to the
    database.

    Args:
        tb_db (sql.TimeblockDB): An empty TimeblockDB instance.
    """
    requests.post(URL, data={"action": "go to sleep"}, timeout=1)
    with tb_db:
        assert tb_db.read_query("SELECT * FROM action") == [
            (1, "go to sleep", None, None, None)
        ]
