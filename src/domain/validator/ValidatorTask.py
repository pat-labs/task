from typing import Dict, List, Optional

from src.domain.config.Error import Error
from src.domain.constants.ConstantsTask import ConstantsTask
from src.domain.enum.TaskLinkedKey import TaskLinkedKey
from src.domain.enum.TaskStatus import TaskStatus
from src.domain.enum.TaskTags import TaskTags
from src.domain.error.BuilderErrorMessage import BuilderErrorMessage
from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.model.Task import Task
from src.domain.validator.Util import Util
from src.domain.validator.ValidatorAudit import ValidatorAudit


class ValidatorTask:

    def __init__(
        self, builder_error: BuilderErrorMessage, validator_audit: ValidatorAudit
    ):
        self.builder_error = builder_error
        self.validator_audit = validator_audit

    def validate(self, task: Task):
        errors = []

        if not task.task_id:
            errors.append(self.builder_error.required("task_id"))
        if not task.title:
            errors.append(self.builder_error.required("title"))

        field_errors = [
            self.validate_task_id(task.task_id),
            self.validate_title(task.title),
            self.validate_detail(task.detail),
            self.validate_status(task.status),
            self.validate_linked_items(task.linked_items),
            self.validate_task_tags(task.task_tags),
            self.validate_user_assigned_id(task.user_assigned_id),
        ]
        errors.extend([e for e in field_errors if e is not None])

        if errors:
            raise ExceptionDomain(errors=errors)

        self.validator_audit.validate(task.user_audit)
        return None

    # ---------------------------------
    # Field validators
    # ---------------------------------

    def validate_task_id(self, task_id: str) -> Optional[Error]:
        if not task_id:
            return None

        if len(task_id) > ConstantsTask.TASK_ID_MAX_SIZE:
            return self.builder_error.max_size(
                "task_id",
                ConstantsTask.TASK_ID_MAX_SIZE,
            )
        return None

    def validate_title(self, title: str) -> Optional[Error]:
        if not title:
            return None

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
        if not status:
            return self.builder_error.required("status")

        if len(status) > ConstantsTask.TASK_STATUS_MAX_SIZE:
            return self.builder_error.max_size(
                "status",
                ConstantsTask.TASK_STATUS_MAX_SIZE,
            )

        if not Util.has_name(TaskStatus, status):
            return self.builder_error.not_in_enum(
                "status",
                TaskStatus._member_names_,
            )

        return None

    def validate_user_assigned_id(self, user_assigned_id: str) -> Optional[Error]:
        if not user_assigned_id:
            return self.builder_error.required("user_assigned_id")
        return self.validator_audit.validate_user_created_id(user_assigned_id)

    def validate_linked_items(
        self,
        linked_items: Dict[TaskLinkedKey, List[str]],
    ) -> Optional[Error]:
        if not isinstance(linked_items, dict):
            return self.builder_error.invalid_format("linked_items", "dict")

        for linked in linked_items.keys():
            if not Util.has_name(TaskLinkedKey, linked):
                return self.builder_error.not_in_enum(
                    "linked_items",
                    TaskLinkedKey._member_names_,
                )
        return None

    def validate_task_tags(
        self,
        task_tags: List[str],
    ) -> Optional[Error]:
        if not isinstance(task_tags, list):
            return self.builder_error.invalid_format("task_tags", "list")

        if Util.has_duplicates(task_tags):
            return self.builder_error.not_unique_values("task_tags")

        for tag in task_tags:
            if not Util.has_name(TaskTags, tag):
                return self.builder_error.not_in_enum(
                    "task_tags",
                    TaskTags._member_names_,
                )
        return None
