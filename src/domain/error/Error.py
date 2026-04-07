from enum import Enum, auto
from typing import NamedTuple, Any, Dict


class ErrorKey(Enum):
    REQUIRED = "Param must be provided: {attr}"
    INVALID_FORMAT = "Param not match with the pattern: {}"

class Error(NamedTuple):
    key: Enum
    cls: str
    attr: str
    value: Any
    data: Dict[str, Any]

    @staticmethod
    def required(cls: str, attr: str, current_value):
        return Error(
            key=ErrorKey.REQUIRED,
            cls=cls,
            attr=attr,
            value=current_value,
            data={"attr": attr}
        )

    @staticmethod
    def max_size(cls: str, attr: str, current_value, expected_value):
        return Error(
            key=ErrorKey.INVALID_FORMAT,
            cls=cls,
            attr=attr,
            value=current_value,
            data={"pattern": f"d/{{{expected_value}}}"}
        )