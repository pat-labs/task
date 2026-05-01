from typing import NamedTuple

from src.domain.constants.ConstantsTask import ConstantsTask
from src.domain.model.Audit import Audit
from src.domain.model.Task import Task


class DtoTaskBase(NamedTuple):
    @staticmethod
    def to_task(identifier: str, title: str, user_wrote_id: str) -> Task:
        audit = Audit.create(
            user_wrote_id=user_wrote_id,
        )
        return Task(
            task_id=identifier,
            title=title,
            status=ConstantsTask.TASK_STATUS_DEFAULT_VALUE,
            task_linked_items=[],
            task_tags=[],
            user_assigned_id=user_wrote_id,
            user_audit=audit,
        )
