"""
Test class file : Validates GET and POST /store/order
"""
import pytest
from data.test_inputs.pets.schemas import GetStoreORderID
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
        """
        Method test case to validate the correct response format and status code
        according to the existence of the given order_id
        """
        self.log.info(f"Input data. order_id {order_id}, is_successfully {is_successfully}")
        def successful_error_code(is_successfully):
            return ApiCodeStatus.OK if is_successfully else ApiCodeStatus.NOT_FOUND
        # 1. Validate request execution as well as the response structure
        self.step_check_response(
            expected_schema=GetStoreORderID.get_successfully_error(is_successfully),
            expected_code_status=successful_error_code(is_successfully),
            callback_method=self.client.get_order,
            order_id=order_id
        )
