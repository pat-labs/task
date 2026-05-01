from __future__ import annotations

from typing import List, NamedTuple

from src.domain.error.BuilderError import BuilderError
from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.model.Task import Task


class DtoTaskHeader(NamedTuple):
    task_id: str
    title: str
    status: str
    task_tags: List[str]
    user_assigned_id: str

    @staticmethod
    def from_list(row: List):
        if len(row) != 5:
            raise ExceptionDomain(
                "Task Header Error", [BuilderError.invalid_size("len_task_header", 5)]
            )
        return DtoTaskHeader(
            task_id=row[0],
            title=row[1],
            task_tags=row[2],
            status=row[3],
            user_assigned_id=row[4],
        )

    @staticmethod
    def to_task_header(task: Task):
        return DtoTaskHeader(
            task_id=task.task_id,
            title=task.title,
            task_tags=task.task_tags,
            status=task.status,
            user_assigned_id=task.user_assigned_id,
        )

    @staticmethod
    def print_table(data: List[NamedTuple]):
        txt = "No data"
        if not data:
            return txt

        headers = DtoTaskHeader._fields
        txt = f" | {' | '.join(headers)} |\n"
        txt += "-" * len(txt) + "\n"

        for task in data:
            row = [str(getattr(task, h, "")) for h in headers]
            txt += f" | {' | '.join(row)} |\n"

        return txt
