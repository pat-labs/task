from enum import Enum
from typing import List, Union, Any


class ExceptionDriven(Exception):
    def __init__(self, error_keys: Union[Enum, List[Enum]], details: str, trace: Any = None):
        super().__init__(details)

        if isinstance(error_keys, Enum):
            error_keys = [error_keys]

        self.keys = [e.name for e in error_keys]
        self.details = details
        self.trace = trace

    def __str__(self) -> str:
        return f"[{', '.join(self.keys)}] {self.details}"
