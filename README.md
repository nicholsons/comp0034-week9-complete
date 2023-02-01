# Week 9 completed code

## Set-up

You will need to a Python environment e.g create and activate a venv.

Install the packages from requirements.txt.

Install the apps: `pip install -e .`

## Completed tests

The completed tests are in the [tests](/tests) directory.

To run the tests enter the folliwing in the Terminal or your IDE.

`python -m pytest -v tests/tests_paralympic_app/ -W ignore::DeprecationWarning`

`python -m pytest -v tests/tests_iris_app/ -W ignore::DeprecationWarning`

The extra flag ignores package deprecation warnings. This is done to reduce the amount of text reported from the tests which hopefully makes it a little easier for you to see the errors that are specific to the test code.
