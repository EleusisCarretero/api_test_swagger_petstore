"""
Common base class file and common utils relates to it 
"""
import json
from src.base_api_client import BaseApiClient
from test_utils.logger_manager import LoggerManager


def get_test_data(test_case):
    with open("data\\test_inputs\\pets\\test_data.json", 'r') as json_file:
        json_info = json.load(json_file).pop()
    return [tuple(v for _, v in _tmp_dict.items()) for _tmp_dict in json_info.get(test_case)]

class BaseTest:
    """
    Base test class
    """
    def setup(self, base_url: str,class_client:BaseApiClient, end_point:str):
        self.client = class_client(base_url=f"{base_url}/{end_point}")
        self.log = LoggerManager.get_logger(self.__class__.__name__)
