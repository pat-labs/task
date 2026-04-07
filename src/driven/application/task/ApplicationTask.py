from typing import Dict, List, Optional

from src.domain.dto.DtoFetchHeadersTasks import DtoFetchHeadersTasks
from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.error.ExceptionDriven import ExceptionDriven
from src.domain.model.config.ModelBootstrap import ModelBootstrap
from src.domain.model.task.ModelTask import ModelTask
from src.domain.validator.ValidatorTask import ValidatorTask


class ApplicationTask:
    def __init__(self, bootstrap: ModelBootstrap):
        self.repository_task = bootstrap.repository_task
        self.validator_task = ValidatorTask(bootstrap.error_key)

    @staticmethod
    def get_template() -> Dict:
        return ModelTask.get_template()._asdict()

    def create(self, task: ModelTask):
        error_domain = self.validator_task.validate_new(task)
        if error_domain:
            raise ExceptionDomain(error_domain)

        error_driven = self.repository_task.create(task)
        if error_driven:
            raise ExceptionDriven(error_driven)

        return None

    def fetch_headers(self) -> List[DtoFetchHeadersTasks]:
        return self.repository_task.fetch_headers_tasks()

    def fetch(self) -> List[ModelTask]:
        return self.repository_task.fetch()

    def update(self, task: ModelTask) -> None:
        error_domain = self.validator_task.validate(task)
        if error_domain:
            raise ExceptionDomain(error_domain)

        error_driven = self.repository_task.update(task)
        if error_driven:
            raise ExceptionDriven(error_driven)

        return None

    def fetch_by_id(self, task_id: str) -> Optional[ModelTask]:
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
            raise ExceptionDriven(error_driven)

        return None
