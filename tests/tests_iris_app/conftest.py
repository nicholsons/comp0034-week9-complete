import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from iris_app import create_app, config


# Used for the Flask routes tests and the Selenium tests
@pytest.fixture(scope="session")
def app():
    """Create a Flask app configured for testing"""
    app = create_app(config.TestConfig)

    yield app


# Used for the Flask route tests
@pytest.fixture(scope="function")
def test_client(app):
    """Create a Flask test test_client"""
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


# Used for the Selenium tests
@pytest.fixture(scope="session")
def chrome_driver():
    """Selenium webdriver with options to support running in GitHub actions
    Note:
        For CI: `headless` not commented out
        For running on your computer: `headless` to be commented out
    """
    options = Options()
    options.add_argument("--headless")
    driver = Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


# Data for any of the tests
@pytest.fixture(scope="module")
def form_data():
    """Data for a prediction.

    Uses: 7.0,3.2,4.7,1.4,versicolor
    """
    form_data_versicolor = {
        "sepal_length": 7.0,
        "sepal_width": 3.2,
        "petal_length": 4.7,
        "petal_width": 1.4,
    }
    yield form_data_versicolor
