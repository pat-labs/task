from logging import Logger
from typing import NamedTuple

from src.domain.config.Env import Env
from src.domain.port.external_service.ServiceUser import ServiceUser
from src.domain.port.Identifier.IdentifierGenerator import IdentifierGenerator
from src.driven.repository.file_system.MyFileSystemCsv import MyFileSystemCsv
from src.driven.repository.postgres.MyPostgres import MyPostgres


class Bootstrap(NamedTuple):
    project_dir: str
    env: Env
    console_log: Logger
    event_log: Logger
    identifier_generator: IdentifierGenerator
    service_user: ServiceUser
    repository_file: MyFileSystemCsv
    repository_postgres: MyPostgres
