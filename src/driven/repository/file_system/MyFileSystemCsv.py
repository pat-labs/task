import csv
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List

from src.domain.constants.Constants import Constants
from src.domain.error.BuilderError import BuilderError
from src.domain.error.ExceptionDriven import ExceptionDriven


class MyFileSystemCsv:
    file_extension = ".csv"
    separator = Constants.CSV_SEPARATOR
    driving_component = "REPOSITORY_FILE_SYSTEM"

    def __init__(
        self, base_path: str, console_log: logging.Logger, event_log: logging.Logger
    ):
        self._base_path = Path(base_path)
        self.console_log = console_log
        self.event_log = event_log

    def build_path(self, schema: str, table: str) -> Path:
        try:
            path = self._base_path / schema / f"{table}{self.file_extension}"
            path.parent.mkdir(parents=True, exist_ok=True)
            return path
        except Exception as e:
            raise ExceptionDriven(
                "Failed to build file path.",
                [BuilderError.runtime_error(str(e))],
            )

    def write(
        self,
        file_path: Path,
        data: Iterable[Dict[str, Any]],
        append: bool = False,
    ) -> None:
        self._write_csv(file_path, data, append)

    def read(self, file_path: Path) -> List[Dict[str, Any]]:
        return self._read_csv(file_path)

    def create_with_headers(self, file_path: Path, headers: List[str]) -> None:
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with file_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=headers, delimiter=self.separator)
                writer.writeheader()

        except Exception as e:
            raise ExceptionDriven(
                "Failed to create CSV with headers.",
                [BuilderError.runtime_error(f"{file_path}: {str(e)}")],
            )

    # -------------------------
    # Internal
    # -------------------------
    def _read_csv(self, file_path: Path) -> List[Dict[str, Any]]:
        try:
            if not file_path.exists():
                return []

            with file_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f, delimiter=self.separator)
                return [dict(row) for row in reader]

        except Exception as e:
            raise ExceptionDriven(
                "Failed to read CSV.",
                [BuilderError.runtime_error(f"{file_path}: {str(e)}")],
            )

    def _write_csv(
        self,
        file_path: Path,
        data: Iterable[Dict[str, Any]],
        append: bool,
    ) -> None:
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            data = list(data)
            if not data:
                file_path.write_text("", encoding="utf-8")
                return

            headers = list(dict.fromkeys(key for row in data for key in row.keys()))
            mode = "a" if append and file_path.exists() else "w"

            with file_path.open(mode, encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=headers,
                    extrasaction="ignore",
                    delimiter=self.separator,
                )

                if mode == "w":
                    writer.writeheader()

                writer.writerows(data)

        except Exception as e:
            raise ExceptionDriven(
                "Failed to write CSV.",
                [BuilderError.runtime_error(f"{file_path}: {str(e)}")],
            )

    @staticmethod
    def parse_from_list(data: List) -> str:
        return "|".join(data)

    @staticmethod
    def parse_to_list(data: str) -> List:
        return data.split("|") if data else []
