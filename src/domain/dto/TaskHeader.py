from typing import List, NamedTuple

from src.domain.model.Task import Task


class TaskHeader(NamedTuple):
    task_id: str
    title: str
    task_tags: List[str]
    status: str
    user_assigned_id: str

    @staticmethod
    def to_task_header(task: Task):
        return TaskHeader(
            task_id=task.task_id,
            title=task.title,
            task_tags=task.task_tags,
            status=task.status,
            user_assigned_id=task.user_assigned_id,
        )

    @staticmethod
    def print_task_table(tasks: List[TaskHeader]):
        txt = "No data"
        if not tasks:
            return txt

        headers = TaskHeader._fields
        txt = f" | {' | '.join(headers)} |"
        txt += "-" * len(txt)

        for task in tasks:
            row = [str(getattr(task, h, "")) for h in headers]
            txt += f" | {' | '.join(row)} |"

        return txt
