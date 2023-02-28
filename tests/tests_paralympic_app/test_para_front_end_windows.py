import subprocess
import pytest
import socket
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def flask_port():
    """Ask OS for a free port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port


@pytest.fixture(scope="module")
def run_app_win(flask_port):
    """Runs the Flask app for live server testing on Windows"""
    server = subprocess.Popen(
        [
            "flask",
            "--app",
            "paralympic_app:create_app('paralympic_app.config.TestConfig')",
            "run",
            "--port",
            str(flask_port),
        ]
    )
    try:
        yield server
    finally:
        server.terminate()


def test_home_page_title(chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    THEN the value of the page title should be "Paralympics Home"
    """
    # Change the url if you configured a different port!
    url = f"http://localhost:{flask_port}"
    chrome_driver.get(url)
    chrome_driver.implicitly_wait(3)
    assert chrome_driver.title == "Paralympics Home"


def test_event_detail_page_selected(chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the id="1"
    THEN a page with the title "Rome" should be displayed
    AND the page should contain an element with the id "highlights"
    should be displayed and contain a text value "First Games"
    """
    url = f"http://localhost:{flask_port}"
    chrome_driver.get(url)
    # Wait until the element with id="1" is on the page  https://www.selenium.dev/documentation/webdriver/waits/ and then click on it
    el_1 = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "1")
    )
    el_1.click()
    # Find the text value of the event highlights
    text = chrome_driver.find_element(By.ID, "highlights").text
    assert "First Games" in text


def test_home_nav_link_returns_home(chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND then the user clicks on the event with the id="1"
    AND then the user clicks on the navbar in the 'Home' link
    THEN the page url should be "http://127.0.0.1:5000/"
    """
    url = f"http://localhost:{flask_port}"
    chrome_driver.get(url)
    # Wait until the element with id="1" is on the page
    # https://www.selenium.dev/documentation/webdriver/waits/
    # and then click on it
    el_1 = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "1")
    )
    el_1.click()
    nav_home = WebDriverWait(chrome_driver, timeout=3).until(
        EC.element_to_be_clickable((By.ID, "nav-home"))
    )
    nav_home.click()
    current_url = chrome_driver.current_url
    assert current_url == url
