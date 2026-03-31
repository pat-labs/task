from __future__ import annotations

from typing import Dict, List, NamedTuple

from src.domain.constants.ConstantsTask import ConstantsTask
from src.domain.enum.TaskStatus import TaskStatus
from src.domain.enum.TaskTags import TaskTags
from src.domain.identifier.Identifier import Identifier
from src.domain.model.ModelAudit import ModelAudit


class ModelTask(NamedTuple):
    task_id: str
    tittle: str
    detail: List[str]
    status: str
    task_ids: List[str]
    task_tags: List[str]
    user_assigned_id: str
    user_audit: Dict

    @staticmethod
    def get_template() -> ModelTask:
        audit = ModelAudit.get_template()._asdict()
        task_id = Identifier.get_datetime_identifier()
        status_default = ConstantsTask.TASK_STATUS_DEFAULT_VALUE

        return ModelTask(
            task_id=task_id,
            tittle="",
            detail=["task"],
            status=status_default,
            task_ids=[],
            task_tags=[],
            user_assigned_id="",
            user_audit=audit,
        )

    @staticmethod
    def empty_model():
        return ModelTask(
            task_id="",
            tittle="",
            detail=[],
            status="",
            task_ids=[],
            task_tags=[],
            user_assigned_id="",
            user_audit={}
        )

    @staticmethod
    def get_status() -> Dict[str, str]:
        return {k: v.value for k, v in TaskStatus.__members__.items()}

    @staticmethod
    def get_tags() -> Dict[str, str]:
        return {k: v.value for k, v in TaskTags.__members__.items()}
