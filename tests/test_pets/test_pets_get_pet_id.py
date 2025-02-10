"""
Test class file : Validates Get pet/{petId}
"""
import json
import pytest
from data.test_inputs.pets.schemas import GetPetIDSchemas
from src.base_api_client import ApiCodeStatus
from tests.base_test import get_test_data
from tests.test_pets.base_test_pets import BaseTestPets


@pytest.mark.Pet
class TestPetsGetPetId(BaseTestPets):
    """
    Pets test class to validate UploadImage related test cases
    """
    @pytest.fixture(autouse=True)
    def setup(self, load_base_url, result):
        super().setup(load_base_url, result)

    @pytest.mark.Smoke
    @pytest.mark.parametrize(
            ("pet_id", "is_valid"),
            get_test_data("test_get_pet_data")
    )
    def test_get_pet_data(self, pet_id, is_valid):
        """
        Method test-case to evaluate the GET request to endpoint '/pet/petId/ when the give
        petId is valid, meaning that exists, or invalid, meaning that does not exists.

        Args:
            pet_id(str): PetId
            is_valid(bool): flag to determinate if the petId is valid or not
        """
        def valid_invalid_code(is_valid):
            return ApiCodeStatus.OK if is_valid else ApiCodeStatus.NOT_FOUND

        # 1. Validate request execution as well as the response structure
        self.step_check_response(
            expected_schema=GetPetIDSchemas.get_valid_invalid(is_valid),
            expected_code_status=valid_invalid_code(is_valid),
            callback_method=self.client.get_pet_by_id,
             pet_id=pet_id
        )
