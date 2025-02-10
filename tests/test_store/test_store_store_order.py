"""
Test class file : Validates GET and POST /store/order
"""
import json
import os
from datetime import datetime, timezone
import pytest
from data.test_inputs.pets.schemas import POST_UPLOAD_IMAGE, GetStoreORderID
from src.base_api_client import ApiCodeStatus
from tests.base_test import get_test_data
from tests.test_store.base_test_store import BaseTestStore


@pytest.mark.Pet
class TestStoreStoreOrder(BaseTestStore):
    """
    Pets test class to validate UploadImage related test cases
    """
    @pytest.fixture(autouse=True)
    def setup(self, load_base_url, result):
        super().setup(load_base_url, result)
    
    @pytest.mark.parametrize(
            ("order_id", "is_successfully"),
            get_test_data("test_store_order")
    )
    def test_store_order(self, order_id, is_successfully):
        def successful_error_code(is_valid):
            return ApiCodeStatus.OK if is_valid else ApiCodeStatus.NOT_FOUND
        # 1. Check response
        response = self.result.check_not_raises_any_exception(
            method=self.client.get_order,
            step_msg=f"Check GET pet data by id {order_id} is executed successfully",
            order_id=order_id
        )
        response_body = json.loads(response.text)
        self.log.info(f"The current message content: {response_body}")
        # 2. Validate schema response in base if it a valid id or a invalid id
        self.step_check_response_body_structure(
            response_body,
            GetStoreORderID.get_successfully_error(is_successfully)
        )
        self.log.info("Wait")

