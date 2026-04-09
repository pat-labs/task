from typing import List, Optional, Protocol

from src.domain.enum.DrivingComponent import DrivingComponent
from src.domain.model.task.Task import Task
from src.domain.model.task.TaskHeader import TaskHeader


class RepositoryTask(Protocol):
    schema: str
    table: str
    driving_component: DrivingComponent

    def entity_exists(self, task_id: str) -> bool:
        pass

    def create(self, task: Task):
        pass

    def fetch_headers_tasks(self) -> List[TaskHeader]:
        pass

    def update(self, task: Task):
        pass

    def fetch_by_id(self, task_id: str) -> Optional[Task]:
        pass

    def delete(self, task_id: str):
        pass

    def fetch(self) -> List[Task]:
        pass
