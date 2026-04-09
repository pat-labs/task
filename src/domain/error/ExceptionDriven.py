from typing import List

from src.domain.config.Error import Error
from src.domain.enum.DrivingComponent import DrivingComponent


class ExceptionDriven(Exception):
    """Base exception for domain-related errors."""

    def __init__(
        self,
        component: DrivingComponent,
        errors: List[Error],
    ):
        self.component = component
        self.errors = errors or []
        super().__init__(self._build_message())

    # -------------------------
    # Private helpers
    # -------------------------
    def _build_message(self) -> str:
        if not self.errors:
            return "Domain exception occurred with no error details."

        return (
            self.component.value
            + ":\n"
            + "\n".join(f"{error.key.value}: {error.message}" for error in self.errors)
        )

    # -------------------------
    # String representation
    # -------------------------
    def __str__(self) -> str:
        return self._build_message()
