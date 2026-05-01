from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.domain.error.Error import Error


class ExceptionDomain(Exception):
    def __init__(self, message: str, errors: List[Error]):
        self.errors = errors
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message + "\n".join([str(e) for e in self.errors])
