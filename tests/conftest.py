"""Модуль с тестами."""

import pytest
from src.main import app as a


@pytest.fixture
def app():

    a.config.from_mapping({'TESTING': True})
    return a


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
