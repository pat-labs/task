from typing import List

from src.domain.config.Error import Error


class ExceptionDomain(Exception):
    def __init__(self, errors: List[Error]):
        self.errors = errors or []
        super().__init__(self._build_message())

    def _build_message(self) -> str:
        if not self.errors:
            return "Domain exception occurred with no error details."

        return "\n".join(f"{error.key.value}-{error.message}" for error in self.errors)

    def __str__(self) -> str:
        return self._build_message()
