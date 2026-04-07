from typing import NamedTuple

from src.driving.config.Env import ModelEnv


class ModelBootstrap(NamedTuple):
    env: ModelEnv
    project_dir: str
