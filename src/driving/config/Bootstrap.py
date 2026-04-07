import os

from src.domain.model.config.ModelBootstrap import ModelBootstrap
from src.driving.config.Env import Env


class Bootstrap:
    @staticmethod
    def load_bootstrap() -> ModelBootstrap:
        # Load environment variables
        env = BuilerEnv.load_env()
        error_key = BuilderErrorKey(os.path.join(project_dir, "resource", "error_key.json"))

        project_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )

        db_path = os.path.join(project_dir, "db")
        repository = MyFileSystem(db_path)
        repository_task = FileSystemTask(repository)

        return ModelBootstrap(project_dir=project_dir, env=env, error_key=error_key)
