from typing import List, NamedTuple

from src.domain.enum.TaskStatus import TaskStatus
from src.domain.model.Task import Task


class TaskBase(NamedTuple):
    task_id: str
    title: str
    sub_task: List[Task]

    @staticmethod
    def to_task_base(tasks: List[Task]):
        tasks = []
        sub_tasks = []
        for task in tasks:
            for sub_task in task.linked_items:
                sub_tasks.append(
                    TaskBase(task_id=task.task_id, title=task.title, sub_task=sub_task)
                )
            tasks.append(
                TaskBase(task_id=task.task_id, title=task.title, sub_task=sub_tasks)
            )
        return tasks

    @staticmethod
    def print_to_md(tasks):
        txt = ""
        tab = 0
        for task in tasks:
            for sub_task in task.sub_task:
                tab = tab + 1
                txt += TaskBase._print_line_task(sub_task, tab)
            txt += TaskBase._print_line_task(task, tab)
        return txt

    @staticmethod
    def _print_line_task(task, tab):
        task_status = "-"
        if task.status == TaskStatus.OPEN:
            task_status = " "
        elif task.status == TaskStatus.CLOSED:
            task_status = "X"

        return f"{"" * tab * 4}[{task_status}] {task.title}"
