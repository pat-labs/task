from typing import NamedTuple

from src.domain.error.BuilderErrorMessage import BuilderErrorMessage
from src.domain.model.config.ModelEnv import ModelEnv
from src.driven.repository.RepositoryTask import RepositoryTask
from src.driven.service.ServiceUser import ServiceUser


class ModelBootstrap(NamedTuple):
    project_dir: str
    env: ModelEnv
    error_key: BuilderErrorMessage
    service_user: ServiceUser
    repository_task: RepositoryTask
