from __future__ import annotations

from typing import NamedTuple

from src.domain.constants.Constants import Constants


class ModelAudit(NamedTuple):
    audit_id: str
    user_wrote_id: str
    updated_at: str
    user_created_id: str
    created_at: str

    @staticmethod
    def get_template() -> ModelAudit:
        audit = ModelAudit(
            audit_id="",
            user_wrote_id="",
            updated_at=Constants.DATE_TIME_FORMAT,
            user_created_id="",
            created_at=Constants.DATE_TIME_FORMAT,
        )
        return audit
