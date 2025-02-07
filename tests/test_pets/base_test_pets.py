from src.pet_client import PetClient
from tests.base_test import BaseTest


class BaseTestPets(BaseTest):
    """
    """
    def setup(self, load_base_url):
        super().setup(load_base_url, PetClient, "pet")