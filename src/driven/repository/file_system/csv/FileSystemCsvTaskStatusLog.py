from typing import List

from src.domain.model.StatusLog import StatusLog
from src.driven.repository.file_system.MyFileSystemCsv import MyFileSystemCsv


class FileSystemCsvTaskStatusLog:
    schema = "tasks"
    table = "tasks_status_log"

    def __init__(self, my_file_system: MyFileSystemCsv) -> None:
        self._fs = my_file_system
        self._path = self._fs.build_path(self.schema, self.table)
        self.console_log = my_file_system.console_log

    # -------------------------
    # Setup
    # -------------------------
    def setup_database(self) -> None:
        self._fs.create_with_headers(self._path, list(StatusLog._fields))
        self.console_log.debug("CSV Tasks Status Log initialized (file cleared).")

    # -------------------------
    # Create
    # -------------------------
    def create(self, status_log: StatusLog) -> None:
        row = status_log._asdict()

        self._fs.write(self._path, [row], append=True)

        self.console_log.debug(
            f"Logged status update for task_id: {status_log.task_id}"
        )

    # -------------------------
    # Read
    # -------------------------
    def fetch_by_id(self, task_id: str) -> List[StatusLog]:
        rows = self._fs.read(self._path)

        history = [
            StatusLog.from_dict(row) for row in rows if row.get("task_id") == task_id
        ]

        history.sort(key=lambda x: x.wrote_at)
        return history

    # -------------------------
    # Delete
    # -------------------------
    def delete(self, task_id: str) -> None:
        rows = self._fs.read(self._path)

        filtered = [row for row in rows if row.get("task_id") != task_id]

        self._fs.write(self._path, filtered)

        self.console_log.debug(f"Deleted status logs for task_id: {task_id}")
