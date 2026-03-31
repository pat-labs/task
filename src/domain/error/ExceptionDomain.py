from enum import Enum
from typing import List


class ExceptionDomain(Exception):
    def __init__(self, exception_keys: List[Enum]):
        self.exceptions = [e.name for e in exception_keys]
