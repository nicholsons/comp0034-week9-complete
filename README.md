# Week 9 completed code

## Set-up

You will need to a Python environment e.g create and activate a venv.

Install the packages from requirements.txt.

Install the apps: `pip install -e .`

## Completed tests

The completed tests are in the [tests](/tests) directory.

Some fixtures for the Selenium tests differ by operating system. To address this, a few changes are made that differ from the tutorial instructions for running the apps:

1. The configuration for Flask is now handled with a Config class object which is an attribute passed to the create_app() function.
2. There are two versions of the Selenium tests for the paralympics_app, one for windows, one for macos. The mac tests will fail on Windows and vice-versa.

    - Windows: `python -m pytest -v tests/tests_paralympic_app/ -W ignore::DeprecationWarning --ignore=tests/tests_paralympic_app/test_para_front_end_macos.py`

    - MacOS: `python -m pytest -v tests/tests_paralympic_app/ -W ignore::DeprecationWarning --ignore=tests/tests_paralympic_app/test_para_front_end_windows.py`

3. To run the iris app tests which uses pytest-flask then the same test code _should_ work Windows and Max: `python -m pytest -v tests/tests_iris_app/ -W ignore::DeprecationWarning`

The `ignore` flag ignores package deprecation warnings. This is done to reduce the amount of text reported from the tests which hopefully makes it a little easier for you to see the errors that are specific to the test code. You can ommit this if you want to see all the warnings.
