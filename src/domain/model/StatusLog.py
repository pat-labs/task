from typing import Any, Dict, NamedTuple

from src.domain.error.BuilderError import BuilderError
from src.domain.error.ExceptionDomain import ExceptionDomain


class StatusLog(NamedTuple):
    task_id: str
    status: str
    user_wrote_id: str
    wrote_at: str

    @staticmethod
    def from_dict(row: Dict[str, Any]):
        try:
            return StatusLog(
                task_id=row["task_id"],
                status=row["status"],
                user_wrote_id=row["user_wrote_id"],
                wrote_at=row["wrote_at"],
            )
        except KeyError as e:
            raise ExceptionDomain(
                "Task Error", [BuilderError.invalid_value("data", e.args[0])]
            )
