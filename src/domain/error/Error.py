from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

from src.domain.enum.ErrorKey import ErrorKey

if TYPE_CHECKING:
    from src.driving.config.BuilderErrorMessage import BuilderErrorMessage


class Error:
    def __init__(self, key: ErrorKey, data: Dict):
        self.key = key
        self.data = data

    def format(self, formatter: Optional[BuilderErrorMessage] = None) -> str:
        if formatter:
            return formatter.format(self)
        return self.key.format(**self.data)

    def __str__(self) -> str:
        attr = self.data.get("attr", "attr not defined")
        message = self.key.format(**self.data)
        return f"{self.key} [{attr}]: {message}"
