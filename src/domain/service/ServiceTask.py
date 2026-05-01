from typing import List, Optional

from src.domain.config.Bootstrap import Bootstrap
from src.domain.dto.DtoTaskHeader import DtoTaskHeader
from src.domain.error.BuilderError import BuilderError
from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.error.ExceptionDriven import ExceptionDriven
from src.domain.model.Audit import Audit
from src.domain.model.Task import Task
from src.domain.validator.ValidatorAudit import ValidatorAudit
from src.domain.validator.ValidatorTask import ValidatorTask
from src.driven.repository.file_system.csv.FileSystemCsvTask import \
    FileSystemCsvTask


class ServiceTask:
    def __init__(self, bootstrap: Bootstrap):
        self.service_user = bootstrap.service_user
        self.console_log = bootstrap.console_log

        self.repository = bootstrap.repository_file
        self.repository_task = FileSystemCsvTask(self.repository)

        self.validator_audit = ValidatorAudit(bootstrap.service_user)
        self.validator_task = ValidatorTask(
            bootstrap.service_user, self.validator_audit
        )

    def create(self, current_task: Task, user_wrote_id: str):
        self.validator_task.validate(current_task)

        audit = Audit.create(user_wrote_id)
        current_task._replace(user_audit=audit)

        error_driven = self.repository_task.create(current_task)
        if error_driven:
            raise ExceptionDriven(self.repository_task.driving_component, error_driven)

        self.console_log.info(
            f"Task {current_task.task_id} created successfully by {user_wrote_id}"
        )
        return None

    def fetch_headers(self) -> List[DtoTaskHeader]:
        return self.repository_task.fetch_headers_tasks()

    def fetch(self) -> List[Task]:
        return self.repository_task.fetch()

    def update(self, current_task: Task, user_wrote_id: str) -> None:
        self.validator_task.validate(current_task)

        audit = Audit.update(current_task.user_audit, user_wrote_id)
        current_task._replace(user_audit=audit)

        error_driven = self.repository_task.update(current_task)
        if error_driven:
            raise ExceptionDriven(self.repository_task.driving_component, error_driven)

        self.console_log.info(
            f"Task {current_task.task_id} updated successfully by {user_wrote_id}"
        )
        return None

    def fetch_by_id(self, task_id: str) -> Optional[Task]:
        error_val = self.validator_task.validate_task_id(task_id)
        if error_val:
            raise ExceptionDomain([error_val])

        return self.repository_task.fetch_by_id(task_id)

    def fetch_by_param(self, key: str, value: str) -> List[DtoTaskHeader]:
        if key == "title":
            return self.repository_task.fetch_by_title(value)
        if key == "status":
            return self.repository_task.fetch_by_status(value)
        if key == "tag":
            return self.repository_task.fetch_by_tag(value)

        raise ExceptionDomain(
            "Service Task Error", [BuilderError.invalid_value("search key", key)]
        )

    def delete(self, task_id: str) -> None:
        error_val = self.validator_task.validate_task_id(task_id)
        if error_val:
            raise ExceptionDomain([error_val])

        error_driven = self.repository_task.delete(task_id)
        if error_driven:
            raise ExceptionDriven(self.repository_task.driving_component, error_driven)

        self.console_log.info(f"Task {task_id} deleted successfully.")
        return None
