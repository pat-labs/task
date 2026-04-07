from __future__ import annotations

from typing import NamedTuple

from src.domain.constants.Constants import Constants
from src.domain.identifier.Identifier import Identifier


class ModelAudit(NamedTuple):
    user_wrote_id: str
    updated_at: str
    user_created_id: str
    created_at: str

    @staticmethod
    def get_template() -> ModelAudit:
        now = Identifier.get_datetime_identifier(Constants.DATE_TIME_FORMAT)
        audit = ModelAudit(
            user_wrote_id="",
            updated_at=now,
            user_created_id="",
            created_at=now,
        )
        return audit

    @staticmethod
    def new_audit(user_wrote_id: str):
        now = Identifier.get_datetime_identifier(Constants.DATE_TIME_FORMAT)
        audit = ModelAudit(
            user_wrote_id=user_wrote_id,
            updated_at=now,
            user_created_id=user_wrote_id,
            created_at=now,
        )
        return audit
