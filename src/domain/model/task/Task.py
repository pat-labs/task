from __future__ import annotations

from typing import Dict, List, NamedTuple

from src.domain.constants.Constants import Constants
from src.domain.constants.ConstantsTask import ConstantsTask
from src.domain.enum.TaskLinkedKey import TaskLinkedKey
from src.domain.enum.TaskStatus import TaskStatus
from src.domain.enum.TaskTags import TaskTags
from src.domain.identifier.Identifier import Identifier
from src.domain.model.Audit import Audit


class Task(NamedTuple):
    task_id: str
    title: str
    detail: List[str]
    status: str
    linked_items: Dict
    task_tags: List[str]
    user_assigned_id: str
    user_audit: Audit

    def create(self, user_wrote_id: str):
        audit = Audit.create(user_wrote_id)
        return self._replace(user_audit=audit)

    def update(self, user_wrote_id: str):
        audit = Audit.update(self.user_audit, user_wrote_id)
        return self._replace(user_audit=audit)

    def as_dict(self) -> Dict:
        task_dict = self._asdict()
        task_dict["user_audit"] = self.user_audit.as_dict()
        return task_dict

    @staticmethod
    def get_identifier() -> str:
        return Identifier.get_datetime_identifier(Constants.DATE_TIME_FORMAT)

    @staticmethod
    def get_template(user_wrote_id: str) -> Task:
        audit = Audit.get_template(user_wrote_id)
        task_id = Task.get_identifier()
        status_default = ConstantsTask.TASK_STATUS_DEFAULT_VALUE

        return Task(
            task_id=task_id,
            title="",
            detail=[],
            status=status_default,
            linked_items={},
            task_tags=[],
            user_assigned_id="",
            user_audit=audit,
        )

    @staticmethod
    def get_status() -> List[str]:
        return TaskStatus._member_names_

    @staticmethod
    def get_tags() -> List[str]:
        return TaskTags._member_names_

    @staticmethod
    def get_linked_key() -> List[str]:
        return TaskLinkedKey._member_names_
