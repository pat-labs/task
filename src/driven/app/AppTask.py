from typing import List, Optional

from src.domain.config.Bootstrap import Bootstrap
from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.error.ExceptionDriven import ExceptionDriven
from src.domain.model.task.Task import Task
from src.domain.model.task.TaskHeader import TaskHeader
from src.domain.validator.ValidatorAudit import ValidatorAudit
from src.domain.validator.ValidatorTask import ValidatorTask


class AppTask:
    def __init__(self, bootstrap: Bootstrap):
        self.repository_task = bootstrap.repository_task
        self.service_user = bootstrap.service_user
        self.validator_audit = ValidatorAudit(
            bootstrap.error_key, bootstrap.service_user
        )
        self.validator_task = ValidatorTask(bootstrap.error_key, self.validator_audit)

    def create(self, current_task: Task, user_wrote_id: str):
        error_domain = self.validator_task.validate(current_task)
        if error_domain:
            raise ExceptionDomain(error_domain)

        task = current_task.create(user_wrote_id)

        error_driven = self.repository_task.create(task)
        if error_driven:
            raise ExceptionDriven(self.repository_task.driving_component, error_driven)

        return None

    def fetch_headers(self) -> List[TaskHeader]:
        return self.repository_task.fetch_headers_tasks()

    def fetch(self) -> List[Task]:
        return self.repository_task.fetch()

    def update(self, current_task: Task, user_wrote_id: str) -> None:
        error_domain = self.validator_task.validate(current_task)
        if error_domain:
            raise ExceptionDomain(error_domain)

        task = current_task.update(user_wrote_id)

        error_driven = self.repository_task.update(task)
        if error_driven:
            raise ExceptionDriven(self.repository_task.driving_component, error_driven)

        return None

    def fetch_by_id(self, task_id: str) -> Optional[Task]:
        error_domain = self.validator_task.validate_task_id(task_id)
        if error_domain:
            raise ExceptionDomain([error_domain])

        return self.repository_task.fetch_by_id(task_id)

    def delete(self, task_id: str) -> None:
        error_domain = self.validator_task.validate_task_id(task_id)
        if error_domain:
            raise ExceptionDomain([error_domain])

        error_driven = self.repository_task.delete(task_id)
        if error_driven:
            raise ExceptionDriven(self.repository_task.driving_component, error_driven)

        return None
