from typing import List

from src.domain.dto.DtoFetchHeadersTasks import DtoFetchHeadersTasks
from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.error.ExceptionDriven import ExceptionDriven
from src.domain.model.ModelTask import ModelTask
from src.domain.validator.ValidatorTask import ValidatorTask
from src.driven.repository.RepositoryTask import RepositoryTask


class ApplicationTask:
    def __init__(self, repository_task: RepositoryTask):
        self.repository_task = repository_task
        self.validator_task = ValidatorTask(self.repository_task)

    @staticmethod
    def get_template():
        return ModelTask.get_template()._asdict()

    def create(self, task: ModelTask) -> None:
        error_domain = self.validator_task.validate(task)
        if error_domain:
            raise ExceptionDomain(error_domain)

        error_driven = self.repository_task.create(task)
        if error_driven:
            raise ExceptionDriven(error_driven)

        return None

    def fetch_headers_tasks(self) -> List[DtoFetchHeadersTasks]:
        return self.repository_task.fetch_headers_tasks()

    def fetch_details_tasks(self) -> List[ModelTask]:
        return self.repository_task.fetch()

    def update(self, task: ModelTask) -> None:
        error_domain = self.validator_task.validate(task)
        if error_domain:
            raise ExceptionDomain(error_domain)

        error_driven = self.repository_task.update(task)
        if error_driven:
            raise ExceptionDriven(error_driven)

        return None

    def delete(self, task_id: str) -> None:
        error_domain = self.validator_task.validate_task_id(task_id)
        if error_domain:
            raise ExceptionDomain([error_domain])

        error_driven = self.repository_task.delete(task_id)
        if error_driven:
            raise ExceptionDriven(error_driven)

        return None


