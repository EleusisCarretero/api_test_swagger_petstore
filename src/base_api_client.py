import requests
from enum import Enum


class ApiCodeStatus(int, Enum):
    OK = 200


class BaseApiClientError(Exception):
    """BaseApiClient Error class"""


class BaseApiClient:
    """Base class in charge to manage api requests"""
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.session()
    
    def get(self, endpoint, **kwargs):
        """GET"""
        response = self.session.get(url=f"{self.base_url}{endpoint}", **kwargs)
        return self._handle_response(response)

    def post(self, endpoint, data=None, json=None, **kwargs):
        """POST"""
        response = self.session.post(f"{self.base_url}{endpoint}", data=data, json=json, **kwargs)
        return self._handle_response(response)

    def put(self, endpoint, data=None, json=None, **kwargs):
        """PUT"""
        response = self.session.put(f"{self.base_url}{endpoint}", data=data, json=json, **kwargs)
        return self._handle_response(response)

    def delete(self, endpoint, **kwargs):
        """DELETE"""
        response = self.session.delete(f"{self.base_url}{endpoint}", **kwargs)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response):
        try:
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            raise BaseApiClientError(f"HTTP Error: {err}, Response: {response.text}")
