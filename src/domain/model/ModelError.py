from typing import NamedTuple

from src.domain.enum.ErrorKey import ErrorKey


class ModelError(NamedTuple):
    key: ErrorKey
    message: str
