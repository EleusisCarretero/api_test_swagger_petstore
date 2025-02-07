import json
import pytest
from tests.test_pets.base_test_pets import BaseTestPets


def get_test_data(test_case):
    with open("data\\test_inputs\\pets\\test_data.json", 'r') as json_file:
        json_info = json.load(json_file).pop()
    return [tuple(v for _, v in _tmp_dict.items()) for _tmp_dict in json_info.get(test_case)]


class TestPetsUploadImages(BaseTestPets):

    @pytest.fixture(autouse=True)
    def setup(self, load_base_url):
        super().setup(load_base_url)

    @pytest.mark.parametrize(
            ("new_image", "ped_id"),
            get_test_data("test_load_pet_image")
    )
    def test_load_pet_image(self, new_image, ped_id):
        response = self.client.update_pet_image(pet_id=ped_id,new_image=new_image)
        self.log.info(f"The current message content: {response.text}")
        assert response.status_code == 200
