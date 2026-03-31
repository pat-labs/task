from typing import List, Optional

from src.domain.constants.ConstantsTask import ConstantsTask
from src.domain.error.ExceptionKeyTask import ExceptionKeyTask
from src.domain.model.ModelTask import ModelTask
from src.driven.repository.RepositoryTask import RepositoryTask


def is_not_set(data: List) -> bool:
    if len(data) != len(set(data)):
        return True
    return False


class ValidatorTask:
    def __init__(self, task_repository: RepositoryTask):
        self.task_repository = task_repository

    def validate(self, task: ModelTask) -> List[ExceptionKeyTask]:
        error = [
            self.validate_task_id(task.task_id),
            self.validate_tittle(task.tittle),
            self.validate_detail(task.detail),
            self.validate_status(task.status),
        ]
        return [e for e in error if e is not None]

    @staticmethod
    def validate_task_id(task_id: str) -> Optional[ExceptionKeyTask]:
        if len(task_id) != ConstantsTask.TASK_ID_MAX_SIZE:
            return ExceptionKeyTask.TASK_ID_INVALID_FORMAT
        return None

    @staticmethod
    def validate_tittle(tittle: str) -> Optional[ExceptionKeyTask]:
        if len(tittle) > ConstantsTask.TASK_TITTLE_MAX_SIZE:
            return ExceptionKeyTask.TASK_TITTLE_INVALID_FORMAT
        return None

    @staticmethod
    def validate_detail(detail: List[str]) -> Optional[ExceptionKeyTask]:
        if len(detail) > ConstantsTask.TASK_DESCRIPTION_MAX_SIZE:
            return ExceptionKeyTask.TASK_DESCRIPTION_INVALID_FORMAT
        return None

    @staticmethod
    def validate_status(status: str) -> Optional[ExceptionKeyTask]:
        if len(status) > ConstantsTask.TASK_STATUS_MAX_SIZE:
            return ExceptionKeyTask.TASK_STATUS_INVALID_FORMAT
        return None

    @staticmethod
    def validate_task_ids(task_ids: List[str]) -> Optional[ExceptionKeyTask]:
        return (
            ExceptionKeyTask.TASK_TASK_IDS_IS_NOT_SET if is_not_set(task_ids) else None
        )

    @staticmethod
    def validate_task_tags(task_tags: List[str]) -> Optional[ExceptionKeyTask]:
        return (
            ExceptionKeyTask.TASK_TASK_TAGS_IS_NOT_SET
            if is_not_set(task_tags)
            else None
        )
