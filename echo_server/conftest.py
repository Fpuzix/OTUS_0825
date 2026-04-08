import pytest


@pytest.fixture
def host():
    return "127.0.0.1"


@pytest.fixture
def port():
    return 8080