from enum import Enum
from typing import Dict, List, Optional, Type

from src.domain.config.Error import Error
from src.domain.constants.ConstantsTask import ConstantsTask
from src.domain.enum.TaskLinkedKey import TaskLinkedKey
from src.domain.enum.TaskStatus import TaskStatus
from src.domain.enum.TaskTags import TaskTags
from src.domain.error.BuilderErrorMessage import BuilderErrorMessage
from src.domain.model.task.Task import Task
from src.domain.validator.ValidatorAudit import ValidatorAudit


def has_duplicates(data: List) -> bool:
    return len(data) != len(set(data))


def has_name(enum_class: Type[Enum], name: str) -> bool:
    return name in enum_class.__members__


class ValidatorTask:

    def __init__(
        self, error_builder: BuilderErrorMessage, validator_audit: ValidatorAudit
    ):
        self.builder_error = error_builder
        self.validator_audit = validator_audit

    # ---------------------------------
    # Full validation
    # ---------------------------------
    def validate(self, task: Task) -> List[Error]:
        if not task.task_id:
            return [self.builder_error.required("task_id")]

        if not task.task_id:
            return [self.builder_error.required("title")]

        errors = self.validator_audit.validate(task.user_audit)

        errors += [
            self.validate_task_id(task.task_id),
            self.validate_title(task.title),
            self.validate_detail(task.detail),
            self.validate_status(task.status),
            self.validate_linked_items(task.linked_items),
            self.validate_task_tags(task.task_tags),
        ]

        return [e for e in errors if e is not None]

    # ---------------------------------
    # Field validators
    # ---------------------------------

    def validate_task_id(self, task_id: str) -> Optional[Error]:
        if len(task_id) > ConstantsTask.TASK_ID_MAX_SIZE:
            return self.builder_error.max_size(
                "task_id",
                ConstantsTask.TASK_ID_MAX_SIZE,
            )

        return None

    def validate_title(self, title: str) -> Optional[Error]:
        if len(title) > ConstantsTask.TASK_TITLE_MAX_SIZE:
            return self.builder_error.max_size(
                "title",
                ConstantsTask.TASK_TITLE_MAX_SIZE,
            )
        return None

    def validate_detail(self, detail: List[str]) -> Optional[Error]:
        if len(detail) > ConstantsTask.TASK_DESCRIPTION_MAX_SIZE:
            return self.builder_error.max_size(
                "detail",
                ConstantsTask.TASK_DESCRIPTION_MAX_SIZE,
            )
        return None

    def validate_status(self, status: str) -> Optional[Error]:
        if len(status) > ConstantsTask.TASK_STATUS_MAX_SIZE:
            return self.builder_error.max_size(
                "status",
                ConstantsTask.TASK_STATUS_MAX_SIZE,
            )

        if not has_name(TaskStatus, status):
            return self.builder_error.not_in_enum(
                "status",
                [status.value for status in TaskStatus],
            )

        return None

    def validate_linked_items(
        self,
        linked_items: Dict[str, str],
    ) -> Optional[Error]:

        for linked in linked_items.keys():
            if not has_name(TaskLinkedKey, linked):
                return self.builder_error.not_in_enum(
                    "linked_items",
                    [linked.value for linked in TaskLinkedKey],
                )

        return None

    def validate_task_tags(
        self,
        task_tags: List[str],
    ) -> Optional[Error]:

        if has_duplicates(task_tags):
            return self.builder_error.not_unique_values(
                "task_tags",
            )

        for tag in task_tags:
            if not has_name(TaskTags, tag):
                return self.builder_error.not_in_enum(
                    "task_tags",
                    [tag.value for tag in TaskTags],
                )

        return None
