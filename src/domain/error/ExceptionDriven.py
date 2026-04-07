from typing import Any, List, Union, Optional

from src.domain.model.ModelError import ModelError


class ExceptionDriven(Exception):
    """Base exception for domain-related errors."""

    def __init__(
            self,
            errors: List[ModelError],
    ):
        self.errors = errors or []
        super().__init__(self._build_message())

    # -------------------------
    # Private helpers
    # -------------------------
    def _build_message(self) -> str:
        if not self.errors:
            return "Domain exception occurred with no error details."

        return "\n".join(
            f"{error.key.value}: {error.message}"
            for error in self.errors
        )

    # -------------------------
    # String representation
    # -------------------------
    def __str__(self) -> str:
        return self._build_message()
