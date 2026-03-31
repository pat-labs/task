from enum import Enum


class ExceptionDriven(Exception):
    def __init__(self, exception_key: Enum):
        self.key_exception = exception_key.name
