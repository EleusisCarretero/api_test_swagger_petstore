from src.pet_client import PetClient
from tests.base_test import BaseTest


class BaseTestPets(BaseTest):
    """
    """
    def setup(self):
        self.client = PetClient(base_url="https://petstore.swagger.io/v2/pet")