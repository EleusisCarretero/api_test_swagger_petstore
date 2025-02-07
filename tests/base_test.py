
from src.base_api_client import BaseApiClient


class BaseTest:
    """
    Base test class
    """
    def setup(self, base_url: str,class_client:BaseApiClient, end_point:str):
        self.client = class_client(base_url=f"{base_url}/{end_point}")