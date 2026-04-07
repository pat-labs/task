from typing import NamedTuple

from src.driving.config.Env import ModelEnv


class ModelBootstrap(NamedTuple):
    project_dir: str
    env: ModelEnv
