"""
Shared fixtures for timeblock package tests.

This module contains the following fixtures:
    - app: Runs the application and Flask server.
    - database: Creates a Database instance.
    - tb_db: An empty TimeblockDB instance.
    - instance: An instance of Action with Action.desc set to "test".
    - driver: A Selenium web driver.
"""
import subprocess
import time
import os
from typing import Generator
from signal import SIGINT

from pytest import fixture
from selenium import webdriver

from constants import TEST_DB_PATH, CHROME_PATH
from timeblock import sql
from timeblock.action import Action


@fixture()
def app() -> Generator[None, None, None]:
    """
    Run application and Flask server for testing.

    This fixture runs the application and Flask server for the duration
    of the test. The application is run in a subprocess which
    is terminated after test is complete.
    """
    with subprocess.Popen(["python", "-m", "timeblock", TEST_DB_PATH]) as proc:
        time.sleep(9)  # prevents requests before server runs
        yield
        proc.send_signal(SIGINT)
    # if test_db_path exists, delete it
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


@fixture()
def database() -> Generator[sql.Database, None, None]:
    """
    Create a Database instance for testing.

    This fixture provides an empty Database instance for testing. The database
    is created in the tests directory and is deleted after the test is
    complete.

    Yields:
        sql.Database: A Database instance.
    """
    yield sql.Database(TEST_DB_PATH)
    os.remove(TEST_DB_PATH)


@fixture
def tb_db() -> Generator[sql.TimeblockDB, None, None]:
    """
    Create an empty TimeblockDB instance for testing.

    The database is created in the tests directory and is deleted after the
    test is complete.

    Yields:
        sql.TimeblockDB: An empty TimeblockDB instance.
    """
    yield sql.TimeblockDB(TEST_DB_PATH)
    os.remove(TEST_DB_PATH)


@fixture
def instance() -> Action:
    """
    Create an instance of Action for testing.

    This fixture returns an instance of Action
    where Action.desc is set to "test".
    The other attributes are not set, and equal None.

    Returns:
        Action: An instance of Action with Action.desc set to "test"
    """
    return Action("test")


@fixture(scope="module")
def driver() -> Generator[webdriver.Chrome, None, None]:
    """
    Create Selenium web driver for testing.

    This fixture uses a Selenium driver to run Chrome in headless mode
    during the tests.

    Yields:
        webdriver.Chrome: A Selenium driver for testing.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.binary_location = CHROME_PATH

    with webdriver.Chrome(options=options) as chromedriver:
        yield chromedriver
        chromedriver.quit()
