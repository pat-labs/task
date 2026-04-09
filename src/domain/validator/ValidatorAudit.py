from datetime import datetime
from typing import List, Optional

from src.domain.config.Error import Error
from src.domain.constants.Constants import Constants
from src.domain.error.BuilderErrorMessage import BuilderErrorMessage
from src.domain.model.Audit import Audit
from src.driven.service.ServiceUser import ServiceUser


def is_not_valid_format_user(user_id: str) -> bool:
    return len(user_id) > Constants.USER_ID_MAX_SIZE


def is_not_valid_datetime_format(date: str):
    try:
        return date != datetime.strptime(date, Constants.DATE_TIME_FORMAT).strftime(
            Constants.DATE_TIME_FORMAT
        )
    except (ValueError, TypeError):
        return True


class ValidatorAudit:

    def __init__(self, error_builder: BuilderErrorMessage, service_user: ServiceUser):
        self.builder_error = error_builder
        self.service_user = service_user

    # ---------------------------------
    # Full validation
    # ---------------------------------
    def validate(self, audit: Audit) -> List[Error]:

        if not audit.user_wrote_id:
            return [self.builder_error.required("user_wrote_id")]

        if not audit.user_wrote_id:
            return [self.builder_error.required("updated_at")]

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

    def _validate_user_id(self, field_name: str, user_id: str) -> Optional[Error]:
        if is_not_valid_format_user(user_id):
            return self.builder_error.max_size(
                field_name,
                Constants.USER_ID_MAX_SIZE,
            )

        if not self.service_user.user_exists(user_id):
            return self.builder_error.entity_not_exists(field_name, user_id)
        return None

    def validate_user_wrote_id(
        self,
        user_wrote_id: str,
    ) -> Optional[Error]:
        return self._validate_user_id("user_wrote_id", user_wrote_id)

    def validate_user_created_id(
        self,
        user_created_id: str,
    ) -> Optional[Error]:
        return self._validate_user_id("user_created_id", user_created_id)

    def validate_updated_at(
        self,
        updated_at: str,
    ) -> Optional[Error]:

        if not updated_at:
            return self.builder_error.required("updated_at")

        if is_not_valid_datetime_format(updated_at):
            return self.builder_error.invalid_format(
                "updated_at",
                "ISO datetime date_format",
            )

        return None

    def validate_created_at(
        self,
        created_at: str,
    ) -> Optional[Error]:

        if not created_at:
            return self.builder_error.required("created_at")

        if is_not_valid_datetime_format(created_at):
            return self.builder_error.invalid_format(
                "created_at",
                "ISO datetime date_format",
            )

        return None
