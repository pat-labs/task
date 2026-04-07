from typing import List, Optional, Protocol

from src.domain.dto.DtoFetchHeadersTasks import DtoFetchHeadersTasks
from src.domain.model.ModelTask import ModelTask


class RepositoryTask(Protocol):
    def entity_exists(self, task_id: str) -> bool:
        pass

    def create(self, task: ModelTask):
        pass

    def fetch_headers_tasks(self) -> List[DtoFetchHeadersTasks]:
        pass

    def update(self, task: ModelTask):
        pass

    def fetch_by_id(self, task_id: str) -> Optional[ModelTask]:
        pass

    def delete(self, task_id: str):
        pass

    def fetch(self) -> List[ModelTask]:
        pass
