from test.domain.model.TestModelAudit import TestModelAudit
from typing import List

from src.domain.dto.DtoFetchHeadersTasks import DtoFetchHeadersTasks
from src.domain.model.ModelTask import ModelTask


class TestModelTask:
    @staticmethod
    def get_model() -> ModelTask:
        audit = TestModelAudit.get_model()
        return ModelTask(
            task_id="2604262141",
            tittle="Create a Task",
            detail=["This is a test task"],
            status="OPEN",
            task_ids=["2604262141"],
            task_tags=["PROJECT"],
            user_assigned_id=audit.user_wrote_id,
            user_audit=audit._asdict(),
        )

    @staticmethod
    def fetch_headers_tasks() -> List[DtoFetchHeadersTasks]:
        task = TestModelTask.get_model()
        return [
            DtoFetchHeadersTasks(
                task_id=task.task_id,
                tittle=task.tittle,
                task_tags=task.task_tags,
                status=task.status,
                user_assigned_id=task.user_assigned_id,
            )
        ]

    @staticmethod
    def fetch() -> List[ModelTask]:
        task = TestModelTask.get_model()
        return [task]