import os
from pathlib import Path

from src.domain.config.Bootstrap import Bootstrap
from src.driven.external_service.MockServiceUser import MockServiceUser
from src.driven.repository.Identifier.BuilderIdentifier import BuildIdentifier
from src.driven.repository.file_system.MyFileSystemCsv import MyFileSystemCsv
from src.driven.repository.postgres.MyPostgres import (MyPostgres,
                                                       PostgresConfig)
from src.driving.config.BuilderEnv import BuilderEnv
from src.driving.config.BuilderLogger import BuilderLogger


class BuilderBootstrap:
    @staticmethod
    def load_bootstrap() -> Bootstrap:
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        project_dir = str(project_root)

        env = BuilderEnv.load_env()

        logger_builder = BuilderLogger(
            console_log_level="INFO", json_log_level="DEBUG", json_log_dir="./logs"
        ).build()
        console_log = logger_builder.get_logger("console_logger")
        event_log = logger_builder.get_logger("json_event_logger")

        web_client_user = MockServiceUser()

        my_postgres_config = PostgresConfig(
            host=env.postgres_host,
            user=env.postgres_user,
            password=env.postgres_password,
            database=env.postgres_db,
            port=env.postgres_port,
            minconn=env.postgres_min_connections,
            maxconn=env.postgres_max_connections,
        )
        #repository_postgres = MyPostgres(my_postgres_config, console_log, event_log)
        repository_postgres = None

        db_path = os.path.join(project_dir, env.filesystem_database_dir)
        repository_file = MyFileSystemCsv(db_path, console_log, event_log)

        return Bootstrap(
            project_dir=project_dir,
            env=env,
            console_log=console_log,
            event_log=event_log,
            identifier_generator=BuildIdentifier,
            service_user=web_client_user,
            repository_file=repository_file,
            repository_postgres=repository_postgres,
        )
