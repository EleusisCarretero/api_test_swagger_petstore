import os
import pytest

def pytest_addoption(parser):
    """
    Defines the costume console inputs to run the tests

    device_name: Device name
    """
    parser.addoption("--base_url", action="store", default=os.getenv("API_BASE_URL"), help="Base Pet store swagger url")


@pytest.fixture(scope="session")
def load_base_url(pytestconfig):
    base_url = pytestconfig.getoption("base_url")
    yield base_url
