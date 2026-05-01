from typing import Any, Dict, List, NamedTuple

from src.domain.error.BuilderError import BuilderError
from src.domain.error.ExceptionDomain import ExceptionDomain


class LinkedItem(NamedTuple):
    task_id: str
    linked_key: str
    linked_value: List

    @staticmethod
    def from_dict(row: Dict[str, Any]):
        try:
            return LinkedItem(
                task_id=row["task_id"],
                linked_key=row["linked_key"],
                linked_value=row["linked_value"],
            )
        except KeyError as e:
            raise ExceptionDomain(
                "LinkedItem Error", [BuilderError.invalid_value("data", e.args[0])]
            )
