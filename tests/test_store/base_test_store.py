"""
BaseTestStore class file and relates
"""
from src.store_client import StoreClient
from tests.base_test import BaseTest


class BaseTestStore(BaseTest):
    """
    Base test class for Store test classes
    """
    def setup(self, load_base_url, result):
        super().setup(load_base_url, StoreClient, "store", result)
