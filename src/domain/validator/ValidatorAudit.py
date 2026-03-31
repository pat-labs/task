from datetime import datetime
from typing import List, Optional

from src.domain.constants.Constants import Constants
from src.domain.enum.ExceptionKey import ExceptionKeyAudit
from src.domain.model.ModelAudit import ModelAudit
from src.driven.repository.RepositoryAudit import RepositoryAudit


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
    def __init__(self, audit_repository: RepositoryAudit):
        self.audit_repository = audit_repository

    def validate(self, audit: ModelAudit) -> List[ExceptionKeyAudit]:
        error = [
            self.validate_user_wrote_id(audit.user_wrote_id),
            self.validate_updated_at(audit.updated_at),
            self.validate_user_created_id(audit.user_created_id),
            self.validate_created_at(audit.created_at),
        ]
        return [e for e in error if e is not None]

    @staticmethod
    def validate_user_wrote_id(user_wrote_id: str) -> Optional[ExceptionKeyAudit]:
        return (
            ExceptionKeyAudit.AUDIT_USER_WROTE_ID_INVALID_FORMAT
            if is_not_valid_user(user_wrote_id)
            else None
        )

    @staticmethod
    def validate_user_created_id(user_created_id: str) -> Optional[ExceptionKeyAudit]:
        return (
            ExceptionKeyAudit.AUDIT_USER_CREATE_ID_INVALID_FORMAT
            if is_not_valid_user(user_created_id)
            else None
        )

    @staticmethod
    def validate_updated_at(updated_at: str) -> Optional[ExceptionKeyAudit]:
        return (
            ExceptionKeyAudit.AUDIT_UPDATE_AT_INVALID_FORMAT
            if is_not_valid_datetime_format(updated_at)
            else None
        )

    @staticmethod
    def validate_created_at(created_at: str) -> Optional[ExceptionKeyAudit]:
        return (
            ExceptionKeyAudit.AUDIT_CREATED_AT_INVALID_FORMAT
            if is_not_valid_datetime_format(created_at)
            else None
        )
