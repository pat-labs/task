from __future__ import annotations

from typing import Dict, List, NamedTuple

from src.domain.error.BuilderError import BuilderError
from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.model.Audit import Audit
from src.domain.model.LinkedItem import LinkedItem
from src.domain.model.StatusLog import StatusLog


class Task(NamedTuple):
    task_id: str
    title: str
    status: str
    task_tags: List
    user_assigned_id: str
    task_linked_items: List
    user_audit: Dict

    @staticmethod
    def from_list(row: List):
        if len(row) != 10:
            raise ExceptionDomain(
                "Task Error", [BuilderError.invalid_size("len_task", 10)]
            )
        return Task(
            task_id=row[0],
            title=row[1],
            status=row[2],
            task_linked_items=row[3],
            task_tags=row[4],
            user_assigned_id=row[5],
            user_audit=Audit(
                user_wrote_id=row[6],
                updated_at=row[7],
                user_created_id=row[8],
                created_at=row[9],
            )._asdict(),
        )

    @staticmethod
    def from_dict(task: Dict) -> Task:
        try:
            audit = Audit.from_dict(task["user_audit"])._asdict()
            return Task(
                task_id=task["task_id"],
                title=task["title"],
                status=task["status"],
                task_linked_items=task["task_linked_items"],
                task_tags=task["task_tags"],
                user_assigned_id=task["user_assigned_id"],
                user_audit=audit,
            )
        except KeyError as e:
            raise ExceptionDomain(
                "Task Error", [BuilderError.invalid_value("data", e.args[0])]
            )

    def get_linked_items(self):
        linked_items = []
        for k, v in self.task_linked_items:
            linked_items.append(
                LinkedItem(task_id=self.task_id, linked_key=k, linked_value=v)
            )
        return linked_items

    def get_status_log(self):
        audit = Audit.from_dict(self.user_audit)
        return StatusLog(
            task_id=self.task_id,
            status=self.status,
            user_wrote_id=audit.user_wrote_id,
            wrote_at=audit.updated_at,
        )
