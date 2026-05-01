from typing import List, Optional, Protocol

from src.domain.dto.DtoTaskHeader import DtoTaskHeader
from src.domain.model.Task import Task


class RepositoryTask(Protocol):
    schema: str
    table: str
    driving_component: str

    def setup_database(self) -> None:
        pass

    # -------------------------
    # Write
    # -------------------------

    def create(self, task: Task):
        pass

    def delete(self, task_id: str) -> None:
        pass

    def update(self, task: Task) -> None:
        pass

    # -------------------------
    # Read
    # -------------------------

    def entity_exists(self, task_id: str) -> bool:
        pass

    def fetch_headers_tasks(self) -> List[DtoTaskHeader]:
        pass

    def fetch(self) -> List[Task]:
        pass

    def fetch_by_id(self, task_id: str) -> Optional[Task]:
        pass

    def fetch_by_ids(self, task_ids: List[str]) -> List[DtoTaskHeader]:
        pass

    def fetch_by_tag(self, tag: str) -> List[DtoTaskHeader]:
        pass

    def fetch_by_title(self, title: str) -> List[DtoTaskHeader]:
        pass

    def fetch_by_status(self, status: str) -> List[DtoTaskHeader]:
        pass
