"""
BaseTestPets class file and relates
"""
from src.pet_client import PetClient
from tests.base_test import BaseTest


class BaseTestPets(BaseTest):
    """
    Base test class for Pets test classes
    """
    def setup(self, load_base_url, result):
        super().setup(load_base_url, PetClient, "pet", result)
