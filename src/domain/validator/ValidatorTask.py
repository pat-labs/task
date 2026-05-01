from typing import List, Optional

from src.domain.constants.ConstantsTask import ConstantsTask
from src.domain.enum.TaskLinkedKey import TaskLinkedKey
from src.domain.enum.TaskStatus import TaskStatus
from src.domain.enum.TaskTags import TaskTags
from src.domain.error.BuilderError import BuilderError
from src.domain.error.Error import Error
from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.model.Audit import Audit
from src.domain.model.LinkedItem import LinkedItem
from src.domain.model.Task import Task
from src.domain.port.external_service.ServiceUser import ServiceUser
from src.domain.validator.Util import Util
from src.domain.validator.ValidatorAudit import ValidatorAudit


class ValidatorTask:

    def __init__(self, service_user: ServiceUser, validator_audit: ValidatorAudit):
        self.service_user = service_user
        self.validator_audit = validator_audit

    def validate(self, task: Task):
        errors: List[Error] = []

        if not task.task_id:
            errors.append(BuilderError.required("task_id"))
        if not task.title:
            errors.append(BuilderError.required("title"))

        field_errors = [
            ValidatorTask.validate_task_id(task.task_id),
            ValidatorTask.validate_title(task.title),
            ValidatorTask.validate_status(task.status),
            ValidatorTask.validate_task_linked_items(task.task_linked_items),
            ValidatorTask.validate_task_tags(task.task_tags),
            self.validator_audit.validate_user_id(
                "user_assigned_id", task.user_assigned_id
            ),
        ]
        errors.extend([e for e in field_errors if e is not None])

        if errors:
            raise ExceptionDomain("Task Validation error", errors=errors)

        audit = Audit.from_dict(task.user_audit)
        self.validator_audit.validate(audit)
        return None

    # ---------------------------------
    # Field validators
    # ---------------------------------

    @staticmethod
    def validate_task_id(task_id: str) -> Optional[Error]:
        if not task_id:
            return None

        if len(task_id) > ConstantsTask.TASK_ID_MAX_SIZE:
            return BuilderError.max_size(
                "task_id",
                ConstantsTask.TASK_ID_MAX_SIZE,
            )
        return None

    @staticmethod
    def validate_title(title: str) -> Optional[Error]:
        if not title:
            return None

        if len(title) > ConstantsTask.TASK_TITLE_MAX_SIZE:
            return BuilderError.max_size(
                "title",
                ConstantsTask.TASK_TITLE_MAX_SIZE,
            )
        return None

    @staticmethod
    def validate_status(status: str) -> Optional[Error]:
        attr = "status"
        if not status:
            return BuilderError.required(attr)

        if len(status) > ConstantsTask.TASK_STATUS_MAX_SIZE:
            return BuilderError.max_size(
                attr,
                ConstantsTask.TASK_STATUS_MAX_SIZE,
            )

        if not Util.has_name(TaskStatus, status):
            return BuilderError.not_in_enum(
                attr,
                status,
                TaskStatus._member_names_,
            )

        return None

    @staticmethod
    def validate_task_linked_items(
        task_linked_items: List[LinkedItem],
    ) -> Optional[Error]:
        attr = "task_linked_items"
        if not isinstance(task_linked_items, list):
            return BuilderError.invalid_format(attr, "list")

        if Util.has_duplicates([t[0] for t in task_linked_items]):
            return BuilderError.not_unique_values(attr)

        for item in task_linked_items:
            if len(item) != 2:
                return BuilderError.invalid_format(attr, "2 items are necessary")
            if not isinstance(item[0], str):
                return BuilderError.invalid_format(attr, "str")
            if not Util.has_name(TaskLinkedKey, item[0]):
                return BuilderError.not_in_enum(
                    attr,
                    item[0],
                    TaskLinkedKey._member_names_,
                )
            if not isinstance(item[1], str):
                return BuilderError.invalid_format(attr, "str")

        return None

    @staticmethod
    def validate_task_tags(
        task_tags: List[str],
    ) -> Optional[Error]:
        attr = "task_tags"
        if not isinstance(task_tags, list):
            return BuilderError.invalid_format(attr, "list")

        if Util.has_duplicates(task_tags):
            return BuilderError.not_unique_values(attr)

        for item in task_tags:
            if not isinstance(item, str):
                return BuilderError.invalid_format(attr, "str")
            if not Util.has_name(TaskTags, item):
                return BuilderError.not_in_enum(
                    attr,
                    item,
                    TaskTags._member_names_,
                )

        return None
