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
        return self.session.get(url=f"{self.base_url}{endpoint}", **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        """POST"""
        return self.session.post(f"{self.base_url}{endpoint}", data=data, json=json, **kwargs)

    def put(self, endpoint, data=None, json=None, **kwargs):
        """PUT"""
        return self.session.put(f"{self.base_url}{endpoint}", data=data, json=json, **kwargs)

    def delete(self, endpoint, **kwargs):
        """DELETE"""
        return self.session.delete(f"{self.base_url}{endpoint}", **kwargs)
