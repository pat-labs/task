from __future__ import annotations

from typing import NamedTuple

from src.domain.enum.ErrorKey import ErrorKey


class Error(NamedTuple):
    key: ErrorKey
    message: str
