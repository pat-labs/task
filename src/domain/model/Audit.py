from __future__ import annotations

from typing import Dict, NamedTuple

from src.domain.constants.Constants import Constants
from src.domain.error.BuilderError import BuilderError
from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.util.HandlerDateTime import HandlerDateTime


class Audit(NamedTuple):
    user_wrote_id: str
    updated_at: str
    user_created_id: str
    created_at: str

    @staticmethod
    def to_audit(user_wrote_id: str):
        now = HandlerDateTime.get_datetime_identifier(Constants.DATE_TIME_FORMAT)
        return Audit(
            user_wrote_id=user_wrote_id,
            updated_at=now,
            user_created_id=user_wrote_id,
            created_at=now,
        )

    @staticmethod
    def create(user_wrote_id: str) -> Dict:
        return Audit.to_audit(user_wrote_id)._asdict()

    @staticmethod
    def update(audit: Dict, user_wrote_id: str) -> Dict:
        now = HandlerDateTime.get_datetime_identifier(Constants.DATE_TIME_FORMAT)
        audit_obj = Audit.from_dict(audit)
        return audit_obj._replace(
            user_wrote_id=user_wrote_id,
            updated_at=now,
        )._asdict()

    @staticmethod
    def from_dict(audit: Dict) -> Audit:
        try:
            return Audit(
                user_wrote_id=audit["user_wrote_id"],
                updated_at=audit["updated_at"],
                user_created_id=audit["user_created_id"],
                created_at=audit["created_at"],
            )
        except KeyError as e:
            raise ExceptionDomain(
                "Audit Error", [BuilderError.invalid_value("audit", e.args[0])]
            )
