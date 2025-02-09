"""
BaseApiClient class file and relates
"""
from enum import Enum
import requests


class ApiCodeStatus(int, Enum):
    """Api requests response codes"""
    OK = 200
    BAD_REQUEST = 400
    UNSUPPORTED_MEDIA_TYPE = 415


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
