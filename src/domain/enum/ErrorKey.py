from enum import Enum


class ErrorKey(str, Enum):
    REQUIRED = "REQUIRED"
    INVALID_FORMAT = "INVALID_FORMAT"
    INVALID_VALUE = "INVALID_VALUE"
    MAX_SIZE = "MAX_SIZE"
