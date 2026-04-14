from logging import Logger
from typing import NamedTuple

from src.domain.config.Env import Env
from src.domain.error.BuilderErrorMessage import BuilderErrorMessage
from src.domain.port.external_service.ServiceUser import ServiceUser
from src.domain.port.repository.RepositoryTask import RepositoryTask


class Bootstrap(NamedTuple):
    project_dir: str
    env: Env
    logger: Logger
    builder_error: BuilderErrorMessage
    service_user: ServiceUser
    repository_task: RepositoryTask
