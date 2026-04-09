import os
from typing import List, Optional

from src.domain.config.Error import Error
from src.domain.model.Audit import Audit
from src.domain.model.task.Task import Task
from src.domain.model.task.TaskHeader import TaskHeader
from src.driving.fyle_system.MyFileSystem import MyFileSystem


class FileSystemTask:
    schema = "task"
    table = "task"

    def __init__(self, my_file_system: MyFileSystem):
        path = os.path.join(
            my_file_system.path,
            self.schema,
            f"{self.table}{my_file_system.file_extension}",
        )
        self._fs = my_file_system.set_path(path)

    def entity_exists(self, task_id: str) -> bool:
        return self.fetch_by_id(task_id) is not None

    def create(self, task: Task) -> Optional[Error]:
        tasks = self._read_all()
        if any(t.task_id == task.task_id for t in tasks):
            return self._fs.error_builder.duplicate_key("task_id", task.task_id)
        tasks.append(task)
        self._write_all(tasks)
        return None

    def fetch_headers_tasks(self) -> List[TaskHeader]:
        tasks = self._read_all()
        return [
            TaskHeader(
                task_id=t.task_id,
                title=t.title,
                task_tags=t.task_tags,
                status=t.status,
                user_assigned_id=t.user_assigned_id,
            )
            for t in tasks
        ]

    def update(self, task: Task) -> Optional[Error]:
        tasks = self._read_all()
        found = False
        for i, t in enumerate(tasks):
            if t.task_id == task.task_id:
                tasks[i] = task
                found = True
                break

        if not found:
            return self._fs.error_builder.entity_not_exists("task_id", task.task_id)

        self._write_all(tasks)
        return None

    def fetch_by_id(self, task_id: str) -> Optional[Task]:
        return next((t for t in self._read_all() if t.task_id == task_id), None)

    def delete(self, task_id: str) -> Optional[Error]:
        tasks = self._read_all()
        initial_count = len(tasks)
        tasks = [t for t in tasks if t.task_id != task_id]

        if len(tasks) == initial_count:
            return self._fs.error_builder.entity_not_exists("task_id", task_id)

        self._write_all(tasks)
        return None

    def fetch(self) -> List[Task]:
        return self._read_all()

    def _read_all(self) -> List[Task]:
        data = self._fs.read()
        if not isinstance(data, list):
            return []

        tasks = []
        for t in data:
            # Reconstruct the nested Audit object
            if "user_audit" in t and isinstance(t["user_audit"], dict):
                t["user_audit"] = Audit(**t["user_audit"])
            tasks.append(Task(**t))
        return tasks

    def _write_all(self, tasks: List[Task]):
        self._fs.write([t.as_dict() for t in tasks])
