from enum import Enum
from typing import List, Optional, Dict, Type

from src.domain.constants.ConstantsTask import ConstantsTask
from src.domain.enum.TaskLinkedKey import TaskLinkedKey
from src.domain.enum.TaskStatus import TaskStatus
from src.domain.enum.TaskTags import TaskTags
from src.domain.error.Error import Error
from src.domain.error.ErrorKey import ErrorKey
from src.domain.model.ModelTask import ModelTask
from src.driven.repository.RepositoryTask import RepositoryTask


def is_not_set(data: List) -> bool:
    if len(data) != len(set(data)):
        return True
    return False


def has_name(enum_class: Type[Enum], name: str) -> bool:
    return name in enum_class.__members__

class ValidatorTask:

    def __init__(self, error_builder: BuilderErrorMessage):
        self.builder_error = error_builder

    # ---------------------------------
    # Create new task (required fields)
    # ---------------------------------
    def validate_new(self, task: ModelTask) -> List[ModelError]:
        errors: List[ModelError] = []

        if not task.task_id:
            errors.append(self.builder_error.required("task_id"))

        if not task.title:
            errors.append(self.builder_error.required("title"))

        return errors

    # ---------------------------------
    # Full validation
    # ---------------------------------
    def validate(self, task: ModelTask) -> List[ModelError]:
        errors = [
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

    def validate_task_id(self, task_id: str) -> Optional[ModelError]:
        if len(task_id) != ConstantsTask.TASK_ID_MAX_SIZE:
            return self.builder_error.max_size(
                "task_id",
                ConstantsTask.TASK_ID_MAX_SIZE,
            )
        return None

    def validate_title(self, title: str) -> Optional[ModelError]:
        if len(title) > ConstantsTask.TASK_TITLE_MAX_SIZE:
            return self.builder_error.max_size(
                "title",
                ConstantsTask.TASK_TITLE_MAX_SIZE,
            )
        return None

    def validate_detail(self, detail: List[str]) -> Optional[ModelError]:
        if len(detail) > ConstantsTask.TASK_DESCRIPTION_MAX_SIZE:
            return self.builder_error.max_size(
                "detail",
                ConstantsTask.TASK_DESCRIPTION_MAX_SIZE,
            )
        return None

    def validate_status(self, status: str) -> Optional[ModelError]:
        if len(status) > ConstantsTask.TASK_STATUS_MAX_SIZE:
            return self.builder_error.max_size(
                "status",
                ConstantsTask.TASK_STATUS_MAX_SIZE,
            )

        if not has_name(TaskStatus, status):
            return self.builder_error.invalid_format(
                "status",
                "valid TaskStatus enum value",
            )

        return None

    def validate_linked_items(
        self,
        linked_items: Dict[str, str],
    ) -> Optional[ModelError]:

        for linked in linked_items.keys():
            if not has_name(TaskLinkedKey, linked):
                return self.builder_error.invalid_format(
                    "linked_items",
                    "valid TaskLinkedKey enum key",
                )

        return None

    def validate_task_tags(
        self,
        task_tags: List[str],
    ) -> Optional[ModelError]:

        if is_not_set(task_tags):
            return self.builder_error.invalid_format(
                "task_tags",
                "unique values",
            )

        for tag in task_tags:
            if not has_name(TaskTags, tag):
                return self.builder_error.invalid_format(
                    "task_tags",
                    "valid TaskTags enum value",
                )

        return None
