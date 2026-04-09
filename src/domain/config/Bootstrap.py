from logging import Logger
from typing import NamedTuple

from src.domain.config.Env import Env
from src.domain.error.BuilderErrorMessage import BuilderErrorMessage
from src.driven.repository.RepositoryTask import RepositoryTask
from src.driven.service.ServiceUser import ServiceUser


class Bootstrap(NamedTuple):
    project_dir: str
    env: Env
    logger: Logger
    error_key: BuilderErrorMessage
    service_user: ServiceUser
    repository_task: RepositoryTask
