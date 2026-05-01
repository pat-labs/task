from typing import List, Optional

from src.domain.dto.DtoTaskHeader import DtoTaskHeader
from src.domain.model.Audit import Audit
from src.domain.model.Task import Task
from src.driven.repository.file_system.csv.FileSystemCsvTaskLinkedItem import \
    FileSystemCsvTaskLinkedItem
from src.driven.repository.file_system.csv.FileSystemCsvTaskStatusLog import \
    FileSystemCsvTaskStatusLog
from src.driven.repository.file_system.MyFileSystemCsv import MyFileSystemCsv


class FileSystemCsvTask:
    schema = "tasks"
    table = "tasks"

    def __init__(self, my_file_system: MyFileSystemCsv) -> None:
        self._fs = my_file_system
        self._path = self._fs.build_path(self.schema, self.table)
        self.console_log = my_file_system.console_log

        self._db_linked_items = FileSystemCsvTaskLinkedItem(my_file_system)
        self._db_status_log = FileSystemCsvTaskStatusLog(my_file_system)

    def setup_database(self) -> None:
        self.console_log.debug("-- INIT database Tasks ---")

        self._fs.create_with_headers(
            self._path,
            list(Task._fields),
        )
        self.console_log.debug("CSV Tasks file initialized (cleared).")

        self._db_linked_items.setup_database()
        self._db_status_log.setup_database()

        self.console_log.info("-- Tasks setup successfully ---")

    # -------------------------
    # Write
    # -------------------------

    def create(self, task: Task) -> None:
        rows = self._fs.read(self._path)

        rows.append(self._to_row(task))
        self._fs.write(self._path, rows)

        if task.get_linked_items():
            self._db_linked_items.create(task.get_linked_items())

        self._db_status_log.create(task.get_status_log())

    def delete(self, task_id: str) -> None:
        rows = self._fs.read(self._path)

        self._fs.write(
            self._path,
            [r for r in rows if r["task_id"] != task_id],
        )

        self._db_linked_items.delete(task_id)
        self._db_status_log.delete(task_id)

    def update(self, task: Task) -> None:
        rows = self._fs.read(self._path)
        updated = False

        for i, row in enumerate(rows):
            if row["task_id"] == task.task_id:
                new_row = self._to_row(task)

                # preserve creation audit
                new_row["user_created_id"] = row["user_created_id"]
                new_row["created_at"] = row["created_at"]

                rows[i] = new_row
                updated = True
                break

        if updated:
            self._fs.write(self._path, rows)

            if task.get_linked_items():
                self._db_linked_items.update(task.get_linked_items())

            self._db_status_log.create(task.get_status_log())

    # -------------------------
    # Read
    # -------------------------
    def fetch(self) -> List[Task]:
        rows = self._fs.read(self._path)
        rows.sort(key=lambda x: x["task_id"], reverse=True)

        return [self._to_entity(row) for row in rows]

    def fetch_by_id(self, task_id: str) -> Optional[Task]:
        rows = self._fs.read(self._path)
        row = next((r for r in rows if r["task_id"] == task_id), None)

        return self._to_entity(row) if row else None

    def fetch_headers_tasks(self) -> List[DtoTaskHeader]:
        return [self._to_header(row) for row in self._fs.read(self._path)]

    def fetch_by_ids(self, task_ids: List[str]) -> List[DtoTaskHeader]:
        return [
            self._to_header(row)
            for row in self._fs.read(self._path)
            if row["task_id"] in task_ids
        ]

    def fetch_by_tag(self, tag: str) -> List[DtoTaskHeader]:
        return [
            self._to_header(row)
            for row in self._fs.read(self._path)
            if tag in MyFileSystemCsv.parse_to_list(row.get("task_tags"))
        ]

    def fetch_by_title(self, title: str) -> List[DtoTaskHeader]:
        return [
            self._to_header(row)
            for row in self._fs.read(self._path)
            if title.lower() in row["title"].lower()
        ]

    def fetch_by_status(self, status: str) -> List[DtoTaskHeader]:
        return [
            self._to_header(row)
            for row in self._fs.read(self._path)
            if status.lower() == row["status"].lower()
        ]

    def entity_exists(self, task_id: str) -> bool:
        rows = self._fs.read(self._path)
        return any(row["task_id"] == task_id for row in rows)

    # -------------------------
    # Mapping Helpers
    # -------------------------
    def _to_row(self, task: Task) -> dict:
        audit = Audit.from_dict(task.user_audit)

        return {
            "task_id": task.task_id,
            "title": task.title,
            "status": task.status,
            "task_tags": MyFileSystemCsv.parse_from_list(task.task_tags),
            "user_assigned_id": task.user_assigned_id,
            "user_wrote_id": audit.user_wrote_id,
            "updated_at": audit.updated_at,
            "user_created_id": audit.user_created_id,
            "created_at": audit.created_at,
        }

    def _to_entity(self, row: dict) -> Task:
        linked_items = self._db_linked_items.fetch_by_id(row["task_id"])

        return Task.from_list(
            [
                row["task_id"],
                row["title"],
                row["status"],
                linked_items,
                MyFileSystemCsv.parse_to_list(row.get("task_tags")),
                row["user_assigned_id"],
                row["user_wrote_id"],
                row["updated_at"],
                row["user_created_id"],
                row["created_at"],
            ]
        )

    def _to_header(self, row: dict) -> DtoTaskHeader:
        return DtoTaskHeader.from_list(
            [
                row["task_id"],
                row["title"],
                MyFileSystemCsv.parse_to_list(row.get("task_tags")),
                row["status"],
                row["user_assigned_id"],
            ]
        )
