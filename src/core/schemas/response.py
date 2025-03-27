from pydantic import BaseModel
from typing import Any, Optional
from enum import Enum

class ReturnCodeEnum(str, Enum):
    SUCCESS = "0"
    ERROR = "1"
    NOT_FOUND = "2"
    BAD_REQUEST = "3"
    INTERNAL_ERROR = "4"

class ResponseSchema(BaseModel):
    return_code: ReturnCodeEnum
    data: Optional[Any] = None
