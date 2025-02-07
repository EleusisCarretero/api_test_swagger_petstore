
from src.base_api_client import BaseApiClient
from test_utils.logger_manager import LoggerManager


class BaseTest:
    """
    Base test class
    """
    def setup(self, base_url: str,class_client:BaseApiClient, end_point:str):
        self.client = class_client(base_url=f"{base_url}/{end_point}")
        self.log = LoggerManager.get_logger(self.__class__.__name__)
        print("Wair")