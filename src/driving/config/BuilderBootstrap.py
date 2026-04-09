import os

from src.domain.config.Bootstrap import Bootstrap
from src.domain.error.BuilderErrorMessage import BuilderErrorMessage
from src.driving.config.BuilderEnv import BuilderEnv
from src.driving.config.BuilderLogger import BuilderLogger
from src.driving.fyle_system.FileSystemTask import FileSystemTask
from src.driving.fyle_system.MyFileSystem import MyFileSystem
from src.driving.web_client.WebClientUser import WebClientUser


class BuilderBootstrap:
    @staticmethod
    def load_bootstrap() -> Bootstrap:
        project_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )

        env = BuilderEnv.load_env()

        # Build the logger using BuilderLogger
        # Passing None to get_logger returns the root logger which now has the JSON formatter
        logger = (
            BuilderLogger(env.log_level, env.log_dir, env.log_to_console)
            .build()
            .get_logger("app")
        )

        error_key = BuilderErrorMessage(
            os.path.join(project_dir, "resource", "error_key.json")
        )

        web_client_user = WebClientUser()

        db_path = os.path.join(project_dir, "db")
        repository_file = MyFileSystem(db_path, error_key)
        repository_file_task = FileSystemTask(repository_file)

        return Bootstrap(
            project_dir=project_dir,
            env=env,
            logger=logger,
            error_key=error_key,
            service_user=web_client_user,
            repository_task=repository_file_task,
        )
