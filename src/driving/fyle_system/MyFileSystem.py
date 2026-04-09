import json
import os
from typing import Dict, List

from src.domain.enum.DrivingComponent import DrivingComponent
from src.domain.error.BuilderErrorMessage import BuilderErrorMessage


class MyFileSystem:
    file_extension = ".json"
    driving_component = DrivingComponent.REPOSITORY

    def __init__(self, path: str, error_builder: BuilderErrorMessage):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        self.error_builder = error_builder

    def set_path(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        return self

    def write(self, json_data: List[Dict]):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    def read(self) -> List[Dict]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
