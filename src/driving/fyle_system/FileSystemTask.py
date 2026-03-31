from typing import List, Optional

from src.domain.dto.DtoFetchHeadersTasks import DtoFetchHeadersTasks
from src.domain.model.ModelTask import ModelTask
from src.driving.fyle_system.MyFileSystem import MyFileSystem


class FileSystemTask:
    folder_sufix = "task"
    file_name = "task"

    def __init__(self, my_file_system: MyFileSystem):
        self._fs = my_file_system + "/" +self.folder_sufix

    def validate(self, task: ModelTask) -> List[str]:
        return []

    def create(self, task: ModelTask):
        self._fs.write(task._asdict())

    def fetch_headers_tasks(self) -> List[DtoFetchHeadersTasks]:
        return self._fs.read(self.file_name)

    def update(self, task: ModelTask):
        self._fs.write(task._asdict())

    def fetch_by_id(self, task_id: str) -> Optional[ModelTask]:
        tasks = self._fs.read(self.file_name)
        for task in tasks:
            if task.task_id == task_id:
                return task
        return None

    def delete(self, task_id: str):
        tasks = self._fs.read(self.file_name)
        for index, task in enumerate(tasks):
            if task.task_id == task_id:
                task[index] = None
        self._fs.write(tasks)

    def fetch(self) -> List[ModelTask]:
        return self._fs.read(self.file_name)