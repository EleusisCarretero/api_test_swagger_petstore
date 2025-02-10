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


GET_PED_ID_INVALID = Schema(
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
    INVALID = GET_PED_ID_INVALID

    @classmethod
    def get_valid_invalid(cls, is_valid):
        """Returns the corresponding schema"""
        return cls.VALID.value if is_valid else cls.INVALID.value
