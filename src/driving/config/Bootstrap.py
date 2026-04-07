import os

from src.domain.model.ModelBootstrap import ModelBootstrap
from src.driving.config.Env import Env


class Bootstrap:
    @staticmethod
    def load_bootstrap() -> ModelBootstrap:
        # Load environment variables
        env = Env.load_env()

        # Determine the project directory (root folder)
        # Assuming current file is at project_root/src/driving/config/Bootstrap.py
        project_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )

        return ModelBootstrap(env=env, project_dir=project_dir)
