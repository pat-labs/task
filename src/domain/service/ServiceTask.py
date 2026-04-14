from typing import List, Optional

from src.domain.config.Bootstrap import Bootstrap
from src.domain.dto.TaskHeader import TaskHeader
from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.error.ExceptionDriven import ExceptionDriven
from src.domain.model.Task import Task
from src.domain.validator.ValidatorAudit import ValidatorAudit
from src.domain.validator.ValidatorTask import ValidatorTask


class ServiceTask:
    def __init__(self, bootstrap: Bootstrap):
        self.builder_error = bootstrap.builder_error
        self.repository_task = bootstrap.repository_task
        self.service_user = bootstrap.service_user
        self.logger = bootstrap.logger

        self.validator_audit = ValidatorAudit(
            bootstrap.builder_error, bootstrap.service_user
        )
        self.validator_task = ValidatorTask(
            bootstrap.builder_error, self.validator_audit
        )

    def create(self, current_task: Task, user_wrote_id: str):
        self.validator_task.validate(current_task)

        task = current_task.create(user_wrote_id)

        error_driven = self.repository_task.create(task)
        if error_driven:
            raise ExceptionDriven(self.repository_task.driving_component, error_driven)

        self.logger.info(f"Task {task.task_id} created successfully by {user_wrote_id}")
        return None

    def fetch_headers(self) -> List[TaskHeader]:
        return self.repository_task.fetch_headers_tasks()

    def fetch(self) -> List[Task]:
        return self.repository_task.fetch()

    def update(self, current_task: Task, user_wrote_id: str) -> None:
        self.validator_task.validate(current_task)

        task = current_task.update(user_wrote_id)

        error_driven = self.repository_task.update(task)
        if error_driven:
            raise ExceptionDriven(self.repository_task.driving_component, error_driven)

        self.logger.info(f"Task {task.task_id} updated successfully by {user_wrote_id}")
        return None

    def fetch_by_id(self, task_id: str) -> Optional[Task]:
        error_val = self.validator_task.validate_task_id(task_id)
        if error_val:
            raise ExceptionDomain([error_val])

        return self.repository_task.fetch_by_id(task_id)

    def fetch_by_param(self, key: str, value: str) -> List[TaskHeader]:
        if key == "title":
            return self.repository_task.fetch_by_title(value)
        if key == "status":
            return self.repository_task.fetch_by_status(value)
        if key == "tag":
            return self.repository_task.fetch_by_tag(value)

        raise ExceptionDomain([self.builder_error.invalid_value("search key", key)])

    def delete(self, task_id: str) -> None:
        error_val = self.validator_task.validate_task_id(task_id)
        if error_val:
            raise ExceptionDomain([error_val])

        error_driven = self.repository_task.delete(task_id)
        if error_driven:
            raise ExceptionDriven(self.repository_task.driving_component, error_driven)

        self.logger.info(f"Task {task_id} deleted successfully.")
        return None
