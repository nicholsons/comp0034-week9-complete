import pytest
import subprocess
import time
import socket
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


# Fixtures for Selenium tests on Windows
# Copied from https://github.com/pytest-dev/pytest-flask/issues/54


@pytest.fixture(scope="module")
def flask_port():
    """Ask OS for a free port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port


@pytest.fixture(scope="module")
def live_server_win(flask_port):
    """Live server for running Flask with Windows"""
    server = subprocess.Popen(
        [
            "flask",
            "--app",
            "iris_app:create_app('iris_app.config.TestConfig')",
            "run",
            "--port",
            str(flask_port),
        ]
    )
    # server takes a while to run
    time.sleep(20)
    try:
        yield server
    finally:
        server.terminate()


def test_server_is_up_and_running(live_server_win, chrome_driver):
    """Check the app is running"""
    home_url = f"http://localhost:{flask_port}"
    response = requests.get(home_url)
    assert response.status_code == 200
    # chrome_driver.get("http://127.0.0.1:5000/")
    # assert chrome_driver.title == "Iris Home"


def test_prediction_returns_value(live_server_win, chrome_driver):
    """
    GIVEN a live_server with the iris predictor app
    WHEN the url for the home page is entered
    AND valid details are entered in the prediction form fields
    AND the form is submitted
    THEN the page content should include the words "You are registered!" and the email address
    """
    iris = {
        "sepal_length": 4.8,
        "sepal_width": 3.0,
        "petal_length": 1.4,
        "petal_width": 0.1,
        "species": "iris-setosa",
    }
    # Go to the home page
    url = f"http://localhost:{flask_port}"
    chrome_driver.get(url)
    # Complete the fields in the form
    sep_len = chrome_driver.find_element(By.NAME, "sepal_length")
    sep_len.send_keys(iris["sepal_length"])
    sep_wid = chrome_driver.find_element(By.NAME, "sepal_width")
    sep_wid.send_keys(iris["sepal_width"])
    pet_len = chrome_driver.find_element(By.NAME, "petal_length")
    pet_len.send_keys(iris["petal_length"])
    pet_wid = chrome_driver.find_element(By.NAME, "petal_width")
    pet_wid.send_keys(iris["petal_width"])
    # Click the submit button
    chrome_driver.find_element(By.ID, "btn-predict").click()
    # Wait for the prediction text to appear on the page
    pt = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "prediction-text")
    )
    # Assert that 'setosa' is in the text value of the <p> element. This assumes the model correctly predicts the species!
    assert iris["species"] in pt.text


def test_register_form_on_submit_returns(live_server_win, chrome_driver):
    """
    GIVEN a live_server with the iris predictor app
    WHEN the url for the register is entered
    AND valid details are entered in the email and password fiels
    AND the form is submitted
    THEN the page content should include the words "You are registered!" and the email address
    """
    pass


def test_register_link_from_nav(live_server_win, chrome_driver):
    """
    GIVEN a live_server with the iris predictor app
    WHEN the url for the homepage is entered
    THEN the page title should equal "Iris Home"
    """
    pass
