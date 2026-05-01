from typing import List, Optional

from src.domain.constants.Constants import Constants
from src.domain.error.BuilderError import BuilderError
from src.domain.error.Error import Error
from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.model.Audit import Audit
from src.domain.port.external_service.ServiceUser import ServiceUser
from src.domain.validator.Util import Util


class ValidatorAudit:

    def __init__(self, service_user: ServiceUser):
        self.service_user = service_user

    def validate(self, audit: Audit):
        errors: List = []

        if not audit.user_wrote_id:
            errors.append(BuilderError.required("user_wrote_id"))

        if not audit.user_wrote_id:
            errors.append(BuilderError.required("updated_at"))

        field_errors = [
            self.validate_user_wrote_id(audit.user_wrote_id),
            ValidatorAudit.validate_updated_at(audit.updated_at),
            self.validate_user_created_id(audit.user_created_id),
            ValidatorAudit.validate_created_at(audit.created_at),
        ]

        errors.extend([e for e in field_errors if e is not None])

        if errors:
            print(len(errors))
            print(f"list error?{"".join([e.key.linked_value for e in errors])}")
            raise ExceptionDomain("Audit Validation error", errors=errors)
        return None

    # ---------------------------------
    # Field validators
    # ---------------------------------

    def validate_user_id(self, field_name: str, user_id: str) -> Optional[Error]:
        if Util.is_not_valid_format_user(user_id):
            return BuilderError.max_size(
                field_name,
                Constants.USER_ID_MAX_SIZE,
            )

        if not self.service_user.user_exists(user_id):
            return BuilderError.entity_not_exists(field_name, user_id)
        return None

    def validate_user_wrote_id(
        self,
        user_wrote_id: str,
    ) -> Optional[Error]:
        return self.validate_user_id("user_wrote_id", user_wrote_id)

    def validate_user_created_id(
        self,
        user_created_id: str,
    ) -> Optional[Error]:
        return self.validate_user_id("user_created_id", user_created_id)

    @staticmethod
    def validate_updated_at(
        updated_at: str,
    ) -> Optional[Error]:
        attr = "updated_at"
        if not updated_at:
            return BuilderError.required(attr)

        if Util.is_not_valid_datetime_format(updated_at):
            return BuilderError.invalid_format(
                attr,
                Constants.DATE_TIME_FORMAT,
            )

        return None

    @staticmethod
    def validate_created_at(
        created_at: str,
    ) -> Optional[Error]:
        attr = "created_at"
        if not created_at:
            return BuilderError.required(attr)

        if Util.is_not_valid_datetime_format(created_at):
            return BuilderError.invalid_format(
                attr,
                Constants.DATE_TIME_FORMAT,
            )

        return None
