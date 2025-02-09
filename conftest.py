import os
import pytest
from test_utils.logger_manager import LoggerManager
from test_utils.config import Config
from test_utils.result_manager import ResultManagerClass


def pytest_addoption(parser):
    """
    Defines the costume console inputs to run the tests

    device_name: Device name
    """
    parser.addoption(
        "--base_url",
        action="store",
        default=os.getenv("API_BASE_URL"),
        help="Base Pet store swagger url"
    )
    parser.addoption(
        "--log_folder",
        action="store",
        default="Logs",
        help="Folder to store logs"
    )


@pytest.fixture(scope="session")
def load_base_url(pytestconfig):
    """
    Function to load the base url from the server
    """
    base_url = pytestconfig.getoption("base_url")
    return base_url


@pytest.fixture(scope="session", autouse=True)
def configure_logging(pytestconfig):
    """
    Fixture that setups the common logger.
    """
    log_folder = pytestconfig.getoption("log_folder")
    Config.log_folder = log_folder
    LoggerManager.setup_logger()


@pytest.fixture(scope="class")
def result():
    """
    Fixture to get the instance of ResultManagerClass, common in all tests.
    """
    return ResultManagerClass()
