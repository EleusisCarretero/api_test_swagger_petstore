
import json
import os
import pytest
from datetime import datetime, timezone

import requests
from src.base_api_client import ApiCodeStatus, BaseApiClientError
from tests.base_test import get_test_data
from tests.test_pets.base_test_pets import BaseTestPets


class TestPetsUploadImages(BaseTestPets):

    @pytest.fixture(autouse=True)
    def setup(self, load_base_url, result):
        super().setup(load_base_url, result)

    @pytest.mark.parametrize(
            ("new_image", "pet_id"),
            get_test_data("test_load_pet_image")
    )
    def test_load_pet_image(self, new_image, pet_id):
        """
        Test case to validate a image has been upload correctly.

        Args:
            new_image(str): path to image to load
            ped_id(str): Pet id
        """
        file_size = os.path.getsize(new_image)
        expected_msg = f"additionalMetadata: null\nFile uploaded to ./{new_image.split("\\")[-1]}, {file_size} bytes"
        timestamp_gmt = datetime.now(timezone.utc)
        expected_headers = {
            'Date': timestamp_gmt.strftime("%a, %d-%m-%Y %H:%M:%S GMT"),
            'Content-Type': 'application/json',
            'Transfer-Encoding': 'chunked',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, DELETE, PUT',
            'Access-Control-Allow-Headers': 'Content-Type, api_key, Authorization',
            'Server': 'Jetty(9.2.9.v20150224)'
        }
        # 1. Check response
        response = self.result.check_not_raises_any_exception(
            method=self.client.update_pet_image,
            step_msg=f"Check image {new_image} has been POST without error to petID {pet_id}",
            pet_id=pet_id,
            new_image=new_image
        )
        self.log.info(f"The current message content: {response.text}")
        # 2. Check the correct status
        self.step_check_code_status(
            actual_status=response.status_code,
            expected_status=ApiCodeStatus.OK
        )
        # 3. Check response message
        actual_response_msg = json.loads(response.text)["message"]
        self.step_check_message_response(
            actual_response_msg=actual_response_msg,
            expected_msg=expected_msg
        )
        # 4. Check header requests response
        self.step_check_headers(
            actual_headers=response.headers,
            expected_headers=expected_headers
        )
    
    def test_load_empty_image(self):
       
        pet_id = 2
        response = self.result.check_not_raises_any_exception(
            method=self.client.update_pet_image,
            step_msg=f"Check POST request without error to petID {pet_id}",
            pet_id=pet_id,
        )
        self.log.info(response)

