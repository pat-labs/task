import json
from pathlib import Path
from typing import Any, Optional

from src.domain.enum.DrivingComponent import DrivingComponent
from src.domain.error.BuilderErrorMessage import BuilderErrorMessage


class MyFileSystem:
    file_extension = ".json"
    driving_component = DrivingComponent.REPOSITORY

    def __init__(self, base_path: str, error_builder: BuilderErrorMessage):
        self._base_path = Path(base_path)
        self.error_builder = error_builder
        self.path: Optional[Path] = None

    def set_file(self, schema: str, table: str) -> "MyFileSystem":
        self.path = self._base_path / schema / f"{table}{self.file_extension}"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        return self

    def write(self, data: Any):
        if not self.path:
            raise RuntimeError("File path not set. Call set_file first.")
        self.write_external(data, self.path)

    def read(self) -> Any:
        if not self.path:
            return []
        return self.read_external(self.path)

    def read_external(self, file_path: Path) -> Any:
        if not file_path.exists():
            return []
        with file_path.open("r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def write_external(self, data: Any, file_path: Path):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
