"""
This module contains tests for the Timeblock web interface.

The module imports the following constants from the constants.py module:
    - URL: The URL of the Flask server.
    - CHROME_PATH: The path to the Chrome browser executable.

This module is using these fixtures from the conftest.py module:
    - app: Runs the application and Flask server for testing.
    - driver: A Selenium driver for testing.

The tests cover the following:
    - Flask application is running.
    - Web interface has an input box.
    - POST requests are successful and the new data is displayed.
    - Chrome driver fixture can reach the web interface.
    - Chrome driver can fill inputs and submit form.
"""


import requests
import pytest
from selenium.webdriver.common.by import By

from constants import URL

pytestmark = pytest.mark.usefixtures("app")


def test_server() -> None:
    """
    Test that Flask application is running.

    If the 'app' fixture is able to serve the Flask application, this test
    will pass.
    """
    r = requests.get(URL, timeout=1)
    assert r.status_code == 200


def test_input_box():
    """Test that web interface has an input box."""
    r = requests.get(URL, timeout=1)
    assert "<input" in r.text


def test_submit():
    """Test that POST requests are successful and new data is displayed."""
    r = requests.post(URL, data={"action": "go to sleep"}, timeout=1)
    assert r.status_code == 200
    assert "go to sleep" in r.text


def test_driver(driver):
    """
    Test that the driver fixture runs and can reach the Flask app.

    If 'Timeblock' is not in the <title> element of the page the driver
    reaches, the test will fail.
    """
    driver.get(URL)
    assert "Timeblock" in driver.title


def test_form(driver):
    """
    Test that Chrome driver can input data into the form and submit it.

    If the page that is returned after submitting form contains the 'action'
    that was input, the test will pass.
    """
    driver.get(URL)
    input_box = driver.find_element(By.ID, "action")
    input_box.send_keys("eat breakfast")
    input_box.submit()
    assert "eat breakfast" in driver.find_elements(By.TAG_NAME, "li")[0].text
