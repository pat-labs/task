import os
from typing import List, Optional

from src.domain.dto.DtoFetchHeadersTasks import DtoFetchHeadersTasks
from src.domain.error.ErrorKeyRepository import ErrorKeyRepository
from src.domain.error.ExceptionDriven import ExceptionDriven
from src.domain.model.ModelTask import ModelTask
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
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._fs = MyFileSystem(path)

    def entity_exists(self, task_id: str) -> bool:
        tasks = self._read_all()
        return any(t.task_id == task_id for t in tasks)

    def create(self, task: ModelTask):
        if self.entity_exists(task.task_id):
            raise ExceptionDriven(ErrorKeyRepository.REPOSITORY_DUPLICATE_KEY)
        tasks = self._read_all()
        tasks.append(task)
        self._write_all(tasks)

    def fetch_headers_tasks(self) -> List[DtoFetchHeadersTasks]:
        tasks = self._read_all()
        return [
            DtoFetchHeadersTasks(
                task_id=t.task_id,
                title=t.title,
                task_tags=t.task_tags,
                status=t.status,
                user_assigned_id=t.user_assigned_id,
            )
            for t in tasks
        ]

    def update(self, task: ModelTask):
        if not self.entity_exists(task.task_id):
            raise ExceptionDriven(ErrorKeyRepository.REPOSITORY_ENTITY_NOT_EXISTS)

        tasks = self._read_all()
        for i, t in enumerate(tasks):
            if t.task_id == task.task_id:
                tasks[i] = task
                break
        self._write_all(tasks)

    def fetch_by_id(self, task_id: str) -> Optional[ModelTask]:
        tasks = self._read_all()
        for t in tasks:
            if t.task_id == task_id:
                return t
        return None

    def delete(self, task_id: str):
        if not self.entity_exists(task_id):
            raise ExceptionDriven(ErrorKeyRepository.REPOSITORY_ENTITY_NOT_EXISTS)

        tasks = self._read_all()
        tasks = [t for t in tasks if t.task_id != task_id]
        self._write_all(tasks)

    def fetch(self) -> List[ModelTask]:
        return self._read_all()

    def _read_all(self) -> List[ModelTask]:
        data = self._fs.read()
        if not isinstance(data, list):
            return []
        return [ModelTask(**t) for t in data]

    def _write_all(self, tasks: List[ModelTask]):
        self._fs.write([t._asdict() for t in tasks])
