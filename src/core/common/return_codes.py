from enum import Enum

class ReturnCode(Enum):
    SUCCESS = 0
    GENERIC_ERROR = 1
    NOT_FOUND = 2
    INVALID_INPUT = 3
    INTERNAL_ERROR = 4
