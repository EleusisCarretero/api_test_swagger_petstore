"""
Common base class file and common utils relates to it 
"""
import re
import json
from typing import Union
from schema import Schema, SchemaError
from test_utils.logger_manager import LoggerManager
from src.base_api_client import ApiCodeStatus, BaseApiClient


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
            if key != "date":
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
        """
        Internal check method to validate the 'Date' header is matching the expected values.
        Considering overall that the time stamp could be differ for some value, for that 'second' is evaluated
        with a tolerance.

        Args:
            actual_header_value(dict): Actual response requests header
            expected_header_value(dict): Expected response requests header
            second_tol(int/float): Seconds tolerance
        """
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
                    step_msg=f"Check {actual_part} is within range of {expected_part} +/- {second_tol}")
            i += 1

    def step_check_response_body_structure(self, current_res_body:dict, expected_structure:Schema):
        """
        Step method to validate that the given response body has the expected structure

        Args:
            current_res_body(dict): Current response body from request
            expected_structure(Schema): Expected response body structure
        
        Raises:
            BaseTestError: In case the current response body does not matches with the expected schema
        """
        step_msg = f"Check the response {expected_structure} matches the expected scheme {current_res_body}"
        self.log.info(step_msg)
        self.result.check_not_raises_any_given_exception(
            expected_structure.validate,
            SchemaError,
            f"Check the response {expected_structure} matches the expected scheme {current_res_body}",
            current_res_body
        )
        assert self.result.step_status
        if not self.result.step_status:
            self.log.error(f"The response body: {current_res_body} does not matches in structure and/or types with the expected {expected_structure}")
            raise BaseTestError("The current response body does not have the expected structure")

    def step_check_response(self, expected_schema:Schema, expected_code_status:ApiCodeStatus, callback_method:callable, **kwargs):
        """
        Step function in charge to validate the request execution as well as to validate the response body
        structure and the status code.

        Args:
            expected_schema(Schema): Expected schema structure to validate response body.
            expected_code_status(ApiCodeStatus): Expected status code from the response.
            callback_method(callable): Client method to execute request.
            kwargs(dict): Optional arguments used by callback_method.
        
        Returns:
            response:
        
        Raises:
            BaseTestError: In case the response from request is 'None'.
        """
        # 1. Check request has been executed successfully and returns a response
        response = self.result.check_not_raises_any_exception(
            method=callback_method,
            step_msg=f"Check GET/POST/PUT/DELETE {callback_method} method is successfully executed by using arguments {kwargs}",
            **kwargs
        )
        if response is None:
            raise BaseTestError("There is no valid response")
        response_body = json.loads(response.text)
        self.log.info(f"The current message content: {response_body}")
        # 2. Validate the response body has the expected structure
        self.step_check_response_body_structure(
            response_body,
            expected_schema
        )
        # 3. Check the correct status
        self.step_check_code_status(
            actual_status=response.status_code,
            expected_status=expected_code_status
        )
        return response
