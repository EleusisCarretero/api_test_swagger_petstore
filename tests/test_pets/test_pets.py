
import pytest
from tests.test_pets.base_test_pets import BaseTestPets


class TestPetsUploadImages(BaseTestPets):

    @pytest.fixture(autouse=True)
    def setup(self, load_base_url):
        super().setup(load_base_url)

    def test_load_pet_image(self):
        new_perrito = "data\\perrito.png"
        response = self.client.update_pet_image(pet_id="2",new_image=new_perrito)
        self.log.info(f"The current message content: {response.text}")
        assert response.status_code == 200
