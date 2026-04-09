from __future__ import annotations

from typing import Dict, NamedTuple

from src.domain.constants.Constants import Constants
from src.domain.identifier.Identifier import Identifier


class Audit(NamedTuple):
    user_wrote_id: str
    updated_at: str
    user_created_id: str
    created_at: str

    @staticmethod
    def get_template(user_wrote_id: str) -> Audit:
        now = Identifier.get_datetime_identifier(Constants.DATE_TIME_FORMAT)
        audit = Audit(
            user_wrote_id=user_wrote_id,
            updated_at=now,
            user_created_id=user_wrote_id,
            created_at=now,
        )
        return audit

    @staticmethod
    def create(user_wrote_id: str) -> Audit:
        return Audit.get_template(user_wrote_id)

    @staticmethod
    def update(audit: Audit, user_wrote_id: str) -> Audit:
        now = Identifier.get_datetime_identifier(Constants.DATE_TIME_FORMAT)
        return audit._replace(
            user_wrote_id=user_wrote_id,
            updated_at=now,
        )

    def as_dict(self) -> Dict:
        return self._asdict()
