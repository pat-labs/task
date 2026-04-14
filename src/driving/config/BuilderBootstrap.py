import os
from pathlib import Path

from src.domain.config.Bootstrap import Bootstrap
from src.domain.error.BuilderErrorMessage import BuilderErrorMessage
from src.driven.external_service.web_client.WebClientUser import WebClientUser
from src.driven.repository.file_system.FileSystemTask import FileSystemTask
from src.driven.repository.file_system.MyFileSystem import MyFileSystem
from src.driving.config.BuilderEnv import BuilderEnv
from src.driving.config.BuilderLogger import BuilderLogger


class BuilderBootstrap:
    @staticmethod
    def load_bootstrap() -> Bootstrap:
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        project_dir = str(project_root)

        env = BuilderEnv.load_env()

        logger = (
            BuilderLogger(env.log_level, env.log_dir, env.log_to_console)
            .build()
            .get_logger("external_service")
        )

        builder_error = BuilderErrorMessage(
            os.path.join(project_dir, env.resource_dir, env.error_file_name)
        )

        web_client_user = WebClientUser()

        db_path = os.path.join(project_dir, "db")
        repository_file = MyFileSystem(db_path, builder_error)
        repository_file_task = FileSystemTask(repository_file)

        return Bootstrap(
            project_dir=project_dir,
            env=env,
            logger=logger,
            builder_error=builder_error,
            service_user=web_client_user,
            repository_task=repository_file_task,
        )
