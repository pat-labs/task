from typing import Optional

from src.domain.config.Error import Error
from src.domain.constants.Constants import Constants
from src.domain.error.BuilderErrorMessage import BuilderErrorMessage
from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.model.Audit import Audit
from src.domain.port.external_service.ServiceUser import ServiceUser
from src.domain.validator.Util import Util


class ValidatorAudit:

    def __init__(self, builder_error: BuilderErrorMessage, service_user: ServiceUser):
        self.builder_error = builder_error
        self.service_user = service_user

    def validate(self, audit: Audit):
        errors = []

        if not audit.user_wrote_id:
            return [self.builder_error.required("user_wrote_id")]

        if not audit.user_wrote_id:
            return [self.builder_error.required("updated_at")]

        field_errors = [
            self.validate_user_wrote_id(audit.user_wrote_id),
            self.validate_updated_at(audit.updated_at),
            self.validate_user_created_id(audit.user_created_id),
            self.validate_created_at(audit.created_at),
        ]

        errors.extend([e for e in field_errors if e is not None])

        if errors:
            raise ExceptionDomain(errors=errors)
        return None

    # ---------------------------------
    # Field validators
    # ---------------------------------

    def _validate_user_id(self, field_name: str, user_id: str) -> Optional[Error]:
        if Util.is_not_valid_format_user(user_id):
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

        if Util.is_not_valid_datetime_format(updated_at):
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

        if Util.is_not_valid_datetime_format(created_at):
            return self.builder_error.invalid_format(
                "created_at",
                "ISO datetime date_format",
            )

        return None
