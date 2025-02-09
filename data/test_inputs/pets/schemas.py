"""
Schema structure variables related to Pets services
"""
from schema import Schema, Use

POST_UPLOAD_IMAGE = Schema(
    {
    "code": Use(int),
    "type": Use(str),
    "message": Use(str)
    }
)
