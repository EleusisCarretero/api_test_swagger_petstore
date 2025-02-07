from src.pet_client import PetClient
import pytest


class TestPets:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = PetClient(base_url="https://petstore.swagger.io/v2/pet")

    def test_load_pet_image(self):
        new_perrito = "data\\perrito.png"
        response = self.client.update_pet_image(pet_id="2",new_image=new_perrito)
        assert response.status_code == 200
