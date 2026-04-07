import os

from src.domain.error.BuilderErrorMessage import BuilderErrorMessage
from src.domain.model.config.ModelBootstrap import ModelBootstrap
from src.driving.config.BuilderEnv import BuilderEnv
from src.driving.fyle_system.FileSystemTask import FileSystemTask
from src.driving.fyle_system.MyFileSystem import MyFileSystem
from src.driving.web_client.WebClientUser import WebClientUser


class Bootstrap:
    @staticmethod
    def load_bootstrap() -> ModelBootstrap:
        project_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )

        env = BuilderEnv.load_env()

        error_key = BuilderErrorMessage(
            os.path.join(project_dir, "resource", "error_key.json")
        )

        web_client_user = WebClientUser()

        db_path = os.path.join(project_dir, "db")
        repository_file = MyFileSystem(db_path)
        repository_file_task = FileSystemTask(repository_file)

        return ModelBootstrap(
            project_dir=project_dir,
            env=env,
            error_key=error_key,
            service_user=web_client_user,
            repository_task=repository_file_task,
        )
