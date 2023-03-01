import requests
import multiprocessing
import pytest
from flask import url_for
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with


# Used for the Selenium tests with MacOS
@pytest.fixture(scope="session")
def init_multiprocessing():
    """Sets multiprocessing to fork once per session.

    If already set once then on subsequent calls a runtime error will be raised which should be ignored.

    Needed in Python 3.8 and later
    """
    try:
        multiprocessing.set_start_method("fork")
    except RuntimeError:
        pass


def test_server_is_up_and_running(init_multiprocessing, live_server):
    """Check the app is running"""
    response = requests.get(url_for("index", _external=True))
    assert b"Iris Home" in response.content
    assert response.status_code == 200


def test_prediction_returns_value(live_server, chrome_driver):
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
    # Go to the home page, you can use the Flask url_for to avoid hard-coding the URL
    chrome_driver.get(url_for("index", _external=True))
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


def test_register_form_on_submit_returns(live_server, chrome_driver):
    """
    GIVEN a live_server with the iris predictor app
    WHEN the url for the register is entered
    AND valid details are entered in the email and password fields
    AND the form is submitted
    THEN the page content should include the words "You are registered!" and the email address
    """
    # Go to the register page
    chrome_driver.get(url_for("register", _external=True))
    # Complete the fields in the form
    email_adress = "test@test.com"
    email = chrome_driver.find_element(By.ID, "email")
    email.send_keys(email_adress)
    password = chrome_driver.find_element(By.ID, "password")
    password.send_keys("testpw")
    # The submit button doesn't have an `id=` but is below the password element
    # https://www.selenium.dev/documentation/webdriver/elements/locators/#below
    submit_button = chrome_driver.find_element(
        locate_with(By.TAG_NAME, "input").below({By.ID: "password"})
    )
    submit_button.click()
    p_tag = chrome_driver.find_element(By.TAG_NAME, "p")
    assert "You are registered!" in p_tag.text
    assert email_adress in p_tag.text


def test_register_link_from_nav(live_server, chrome_driver):
    """
    GIVEN a live_server with the iris predictor app
    WHEN the url for the homepage is entered
    THEN the page title should equal "Iris Home"
    """
    pass
