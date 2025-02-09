"""
Common base class file and common utils relates to it 
"""
import re
import json
from typing import Union
from src.base_api_client import ApiCodeStatus, BaseApiClient
from test_utils.logger_manager import LoggerManager


def get_test_data(test_case):
    """
    Common method to load test data for specific test case from 'test_data.json'

    Args:
        test_case(str): Test case key name.

    Returns
        List: List of tuples with parametrized parameters for test cases
    """
    with open("data\\test_inputs\\pets\\test_data.json", 'r', encoding="utf-8") as json_file:
        json_info = json.load(json_file).pop()
    return [tuple(v for _, v in tmp_dict.items()) for tmp_dict in json_info.get(test_case)]


class BaseTestError(Exception):
    """
    BaseTest error class
    """


class BaseTest:
    """
    Base test class
    Attributes:
        client(BaseApiClient): Type class which inherits from BaseApiClient and that helps as interface over the specific clients.
        log(LoggerManager): it is an stance of logger.
        result(ResultManagerClass): is is an instance to manage assertions and matches.
    """
    def setup(self, base_url: str,class_client:BaseApiClient, end_point:str, result):
        self.client = class_client(base_url=f"{base_url}/{end_point}")
        self.log = LoggerManager.get_logger(self.__class__.__name__)
        self.result = result

    def step_check_code_status(self, actual_status: Union [ApiCodeStatus, int], expected_status:ApiCodeStatus):
        """
        Step function to validate the actual code status from a request.

        Args:
            actual_status: Current code status from response
            expected_status: Expected code status the response shall give back.
        """
        self.result.check_equals_to(
            actual_value=actual_status,
            expected_value=expected_status,
            step_msg=f"Check the actual code status: {actual_status} has the expected code status: {expected_status}")
        assert self.result.step_status
    
    def step_check_message_response(self, actual_response_msg: str, expected_msg: str):
        """
        Step function to check the actual response message is the expected.

        Args:
            actual_response_msg(str): Actual response message from requests
            expected_msg(str): Expected response from request
        """
        self.result.check_equals_to(
            actual_value=actual_response_msg,
            expected_value=expected_msg,
            step_msg=f"Check the actual response message: {actual_response_msg} is equals to the expected response message: {expected_msg}")
        assert self.result.step_status
    
    def step_check_headers(self, actual_headers:dict, expected_headers:dict):
        """
        Step function to validate the header from requests response.

        Args:
            actual_headers(dict): Actual response requests header
            expected_headers(dict): Expected response requests header
        """
        # 1. Check the both lengths
        actual_header_len = len(actual_headers)
        expected_header_len = len(expected_headers)
        step_msg = f"Check the actual headers len: {actual_header_len} is equals to the expected header len: {expected_header_len}"
        self.log.info(step_msg)
        self.result.check_equals_to(
            actual_value=actual_header_len,
            expected_value=expected_header_len,
            step_msg=step_msg
        )
        assert self.result.step_status
        if not self.result.step_status:
            raise BaseTestError("The actual and expected headers dictionary have different length")
        # 2. Check the content of both dictionaries
        for key, expected_header_value in expected_headers.items():
            actual_header_value = actual_headers[key]
            if key != "Date":
                step_msg = f"Check the actual header {actual_header_value} vale is equal to the expected header {expected_header_value}"
                self.log.info(step_msg)
                self.result.check_equals_to(
                    actual_value=actual_header_value,
                    expected_value=expected_header_value,
                    step_msg=step_msg
                )
            else:
                self._check_header_date(
                    actual_header_value=actual_header_value,
                    expected_header_value=expected_header_value
                )
            assert self.result.step_status
    
    def _check_header_date(self, actual_header_value, expected_header_value, second_tol=1):

        pattern = r'[:, ]+'
        actual_date_parts = re.split(pattern, actual_header_value)
        expected_date_parts = re.split(pattern, expected_header_value)
        step_msg = f"Check the actual Date header {actual_header_value} is a value close to {expected_header_value}"
        self.log.info(step_msg)
        i=0
        for actual_part, expected_part in zip(actual_date_parts, expected_date_parts):
            if i != 6:
                self.result.check_equals_to(
                    actual_value=actual_part,
                    expected_value=expected_part,
                    step_msg=f"Check {actual_part} is equals to {expected_part}"
                )
            else:
                self.result.check_within_range(
                    actual_value=int(actual_part),
                    expected_value=int(expected_part),
                    within_range=second_tol,
                    step_msg=f"Check {actual_part} is within range of {expected_part} +/- second_tol")
            i += 1
