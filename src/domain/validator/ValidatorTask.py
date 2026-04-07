from enum import Enum
from typing import List, Optional, Dict, Type

from src.domain.constants.ConstantsTask import ConstantsTask
from src.domain.enum.TaskLinkedKey import TaskLinkedKey
from src.domain.enum.TaskStatus import TaskStatus
from src.domain.enum.TaskTags import TaskTags
from src.domain.error.Error import Error
from src.domain.error.ErrorKeyTask import ErrorKeyTask
from src.domain.model.ModelTask import ModelTask
from src.driven.repository.RepositoryTask import RepositoryTask


def is_not_set(data: List) -> bool:
    if len(data) != len(set(data)):
        return True
    return False


def has_name(enum_class: Type[Enum], name: str) -> bool:
    return name in enum_class.__members__

class ValidatorTask:
    def __init__(self, task_repository: RepositoryTask):
        self.task_repository = task_repository

    def validate_new(self, task: ModelTask) -> List[Error]:
        error = []
        if not task.task_id:
            error.append(Error.required("ValidatorTask", "task_id", task.task_id))
        if not task.title:
            error.append(Error.required("ValidatorTask", "title", task.title))
        return error


    def validate(self, task: ModelTask) -> List[Error]:
        error = [
            self.validate_task_id(task.task_id),
            self.validate_title(task.title),
            self.validate_detail(task.detail),
            self.validate_status(task.status),
        ]
        return [e for e in error if e is not None]

    @staticmethod
    def validate_task_id(task_id: str):
        if len(task_id) != ConstantsTask.TASK_ID_MAX_SIZE:
            return ErrorKeyTask.TASK_ID_INVALID_FORMAT
        return None

    @staticmethod
    def validate_title(title: str) -> Optional[ErrorKeyTask]:
        if len(title) > ConstantsTask.TASK_TITLE_MAX_SIZE:
            return ErrorKeyTask.TASK_TITLE_INVALID_FORMAT
        return None

    @staticmethod
    def validate_detail(detail: List[str]) -> Optional[ErrorKeyTask]:
        if len(detail) > ConstantsTask.TASK_DESCRIPTION_MAX_SIZE:
            return ErrorKeyTask.TASK_DESCRIPTION_INVALID_FORMAT
        return None

    @staticmethod
    def validate_status(status: str) -> Optional[ErrorKeyTask]:
        if len(status) > ConstantsTask.TASK_STATUS_MAX_SIZE:
            return ErrorKeyTask.TASK_STATUS_INVALID_FORMAT
        if not has_name(TaskStatus, status):
            return ErrorKeyTask.TASK_STATUS_INVALID_VALUE
        return None

    @staticmethod
    def validate_linked_items(linked_items: Dict[str, str]) -> Optional[ErrorKeyTask]:
        for linked in linked_items.keys():
            if not has_name(TaskLinkedKey, linked):
                return ErrorKeyTask.TASK_LINKED_ITEMS_INVALID_VALUE
        return None

    @staticmethod
    def validate_task_tags(task_tags: List[str]) -> Optional[ErrorKeyTask]:
        if is_not_set(task_tags):
            return ErrorKeyTask.TASK_TASK_TAGS_IS_NOT_SET
        for tag in task_tags:
            if not has_name(TaskTags, tag):
                return ErrorKeyTask.TASK_TAGS_INVALID_VALUE
        return None
