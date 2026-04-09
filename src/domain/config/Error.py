from __future__ import annotations

from typing import NamedTuple, Union

from src.domain.enum.ErrorKey import ErrorKey
from src.domain.enum.ErrorKeyRepository import ErrorKeyRepository


class Error(NamedTuple):
    key: Union[ErrorKey, ErrorKeyRepository]
    message: str
