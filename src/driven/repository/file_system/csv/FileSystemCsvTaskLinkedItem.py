from typing import List

from src.domain.model.LinkedItem import LinkedItem
from src.driven.repository.file_system.MyFileSystemCsv import MyFileSystemCsv


class FileSystemCsvTaskLinkedItem:
    schema = "tasks"
    table = "task_linked_items"

    def __init__(self, my_file_system: MyFileSystemCsv) -> None:
        self._fs = my_file_system
        self._path = self._fs.build_path(self.schema, self.table)
        self.console_log = my_file_system.console_log

    # -------------------------
    # Setup
    # -------------------------
    def setup_database(self) -> None:
        self._fs.create_with_headers(
            self._path,
            list(LinkedItem._fields),
        )
        self.console_log.debug("CSV Tasks Linked Items file initialized with headers.")

    # -------------------------
    # Create
    # -------------------------
    def create(self, linked_items: List[LinkedItem]) -> None:
        if not linked_items:
            return

        rows = [item._asdict() for item in linked_items]

        self._fs.write(self._path, rows, append=True)

        self.console_log.debug(f"Appended {len(linked_items)} linked items to CSV.")

    # -------------------------
    # Read
    # -------------------------
    def fetch_by_id(self, task_id: str) -> List[LinkedItem]:
        rows = self._fs.read(self._path)

        found_items = [
            LinkedItem.from_dict(row) for row in rows if row.get("task_id") == task_id
        ]

        # Keep previous behavior
        found_items.sort(key=lambda x: x.linked_key, reverse=True)

        self.console_log.debug(
            f"Fetched {len(found_items)} linked items for task_id: {task_id}."
        )
        return found_items

    # -------------------------
    # Delete
    # -------------------------
    def delete(self, task_id: str) -> None:
        rows = self._fs.read(self._path)

        filtered = [row for row in rows if row.get("task_id") != task_id]

        self._fs.write(self._path, filtered)

        self.console_log.debug(f"Deleted linked items for task_id: {task_id}.")

    # -------------------------
    # Update
    # -------------------------
    def update(self, linked_items: List[LinkedItem]) -> None:
        if not linked_items:
            return

        task_id = linked_items[0].task_id

        rows = self._fs.read(self._path)
        remaining = [row for row in rows if row.get("task_id") != task_id]

        updated = remaining + [item._asdict() for item in linked_items]

        self._fs.write(self._path, updated)

        self.console_log.debug(f"Updated linked items for task_id: {task_id}.")
