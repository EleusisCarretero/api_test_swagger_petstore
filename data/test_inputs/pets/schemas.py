"""
Schema structure variables related to Pets services
"""
from enum import Enum
from schema import Schema, Use, And


POST_UPLOAD_IMAGE = Schema(
    {
        "code": Use(int),
        "type": Use(str),
        "message": Use(str)
    }
)


GET_PET_ID_VALID = Schema(
    {
        "id": Use(int),
        "category": {
            "id": Use(int),
            "name": Use(str)
        },
        "name": Use(str),
        "photoUrls": [
            Use(str)
        ],
        "tags": [
            {
            "id": Use(int),
            "name": Use(str)
            }
        ],
        "status": And(Use(str), lambda x: x in ["available", "sold", "pending"])
    }
)


GET_PET_ID_INVALID = Schema(
    {
        "code": Use(int),
        "type": And(Use(str), lambda x: x == "error"),
        "message": And(Use(str), lambda x: x == "Pet not found"),
    }
)


class GetPetIDSchemas(Enum):
    """
    Enum for valid or invalid schemas
    """
    VALID = GET_PET_ID_VALID
    INVALID = GET_PET_ID_INVALID

    @classmethod
    def get_valid_invalid(cls, is_valid):
        """Returns the corresponding schema"""
        return cls.VALID.value if is_valid else cls.INVALID.value


GET_ORDER_ID_SUCCESSFUL = Schema(
    {
        "id": Use(int),
        "petId": Use(int),
        "quantity": Use(int),
        "shipDate": Use(str),
        "status": And(Use(str), lambda x: x in ["approved", "delivered", "placed"]),
        "complete": Use(bool)
    }
)

GET_ORDER_ID_ERROR = Schema(
    {
        "code": Use(int),
        "type": "error",
        "message": "Order not found"
    }
)


class GetStoreORderID(Enum):
    """
    Enum successfully and error
    """
    SUCCESSFULLY = GET_ORDER_ID_SUCCESSFUL
    ERROR = GET_ORDER_ID_ERROR

    @classmethod
    def get_successfully_error(cls, is_valid):
        """Returns the corresponding schema"""
        return cls.SUCCESSFULLY.value if is_valid else cls.ERROR.value
