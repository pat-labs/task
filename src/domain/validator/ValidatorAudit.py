from datetime import datetime
from typing import List, Optional

from src.domain.constants.Constants import Constants
from src.domain.error.BuilderErrorMessage import BuilderErrorMessage
from src.domain.model.ModelAudit import ModelAudit
from src.domain.model.ModelError import ModelError


def is_not_valid_user(user_id: str) -> bool:
    if len(user_id) != Constants.USER_ID_MAX_SIZE:
        return True
    return False


def is_not_valid_datetime_format(date: str):
    try:
        if date != datetime.strptime(date, Constants.DATE_TIME_FORMAT).strftime(
                Constants.DATE_TIME_FORMAT
        ):
            raise ValueError
        return False
    except ValueError:
        return True


class ValidatorAudit:

    def __init__(self, error_builder: BuilderErrorMessage):
        self.builder_error = error_builder

    # ---------------------------------
    # Create new audit (required fields)
    # ---------------------------------
    def validate_new(self, audit: ModelAudit) -> List[ModelError]:
        errors: List[ModelError] = []

        if not audit.user_wrote_id:
            errors.append(self.builder_error.required("user_wrote_id"))

        return errors

    # ---------------------------------
    # Full validation
    # ---------------------------------
    def validate(self, audit: ModelAudit) -> List[ModelError]:

        errors = [
            self.validate_user_wrote_id(audit.user_wrote_id),
            self.validate_updated_at(audit.updated_at),
            self.validate_user_created_id(audit.user_created_id),
            self.validate_created_at(audit.created_at),
        ]

        return [e for e in errors if e is not None]

    # ---------------------------------
    # Field validators
    # ---------------------------------

    def validate_user_wrote_id(
            self,
            user_wrote_id: str,
    ) -> Optional[ModelError]:

        if not user_wrote_id:
            return self.builder_error.required("user_wrote_id")

        if is_not_valid_user(user_wrote_id):
            return self.builder_error.invalid_format(
                "user_wrote_id",
                "valid user id format",
            )

        return None

    def validate_user_created_id(
            self,
            user_created_id: str,
    ) -> Optional[ModelError]:

        if not user_created_id:
            return self.builder_error.required("user_created_id")

        if is_not_valid_user(user_created_id):
            return self.builder_error.invalid_format(
                "user_created_id",
                "valid user id format",
            )

        return None

    def validate_updated_at(
            self,
            updated_at: str,
    ) -> Optional[ModelError]:

        if not updated_at:
            return self.builder_error.required("updated_at")

        if is_not_valid_datetime_format(updated_at):
            return self.builder_error.invalid_format(
                "updated_at",
                "ISO datetime format",
            )

        return None

    def validate_created_at(
            self,
            created_at: str,
    ) -> Optional[ModelError]:

        if not created_at:
            return self.builder_error.required("created_at")

        if is_not_valid_datetime_format(created_at):
            return self.builder_error.invalid_format(
                "created_at",
                "ISO datetime format",
            )

        return None
