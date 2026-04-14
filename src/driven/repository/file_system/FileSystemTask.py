from typing import List, Optional

from src.domain.dto.TaskHeader import TaskHeader
from src.domain.enum.DrivingComponent import DrivingComponent
from src.domain.enum.TaskLinkedKey import TaskLinkedKey
from src.domain.error.ExceptionDriven import ExceptionDriven
from src.domain.model.Audit import Audit
from src.domain.model.Task import Task
from src.driven.repository.file_system.MyFileSystem import MyFileSystem


class FileSystemTask:
    schema = "task"
    table = "task"
    view_tag_table = "view_task_by_tag"
    view_sub_task_table = "view_task_by_sub_task"
    driving_component: DrivingComponent

    def __init__(self, my_file_system: MyFileSystem):
        self._fs = my_file_system.set_file(self.schema, self.table)
        self.driving_component = my_file_system.driving_component

    def entity_exists(self, task_id: str) -> bool:
        return self.fetch_by_id(task_id) is not None

    def create(self, task: Task) -> None:
        tasks = self.fetch()
        if any(t.task_id == task.task_id for t in tasks):
            raise ExceptionDriven(
                self._fs.driving_component,
                [self._fs.error_builder.duplicate_key("task_id", task.task_id)],
            )
        tasks.append(task)
        self._write_all(tasks)
        self.create_views(tasks)
        return None

    def fetch_headers_tasks(self) -> List[TaskHeader]:
        return [TaskHeader.to_task_header(t) for t in self.fetch()]

    def update(self, task: Task) -> None:
        tasks = self.fetch()
        found = False
        for i, t in enumerate(tasks):
            if t.task_id == task.task_id:
                tasks[i] = task
                found = True
                break

        if not found:
            raise ExceptionDriven(
                self._fs.driving_component,
                [self._fs.error_builder.entity_not_exists("task_id", task.task_id)],
            )

        self._write_all(tasks)
        self.create_views(tasks)
        return None

    def fetch_by_id(self, task_id: str) -> Optional[Task]:
        return next((t for t in self.fetch() if t.task_id == task_id), None)

    def fetch_by_ids(self, task_ids: List[str]) -> List[TaskHeader]:
        return [
            TaskHeader.to_task_header(t) for t in self.fetch() if t.task_id in task_ids
        ]

    def fetch_by_tag(self, tag: str) -> List[TaskHeader]:
        view_path = self._fs.path.parent / f"{self.view_tag_table}.json"
        view_data = self._fs.read_external(view_path)
        if not isinstance(view_data, dict):
            return []
        task_ids = view_data.get(tag, [])
        if task_ids:
            return self.fetch_by_ids(task_ids)
        return []

    def fetch_by_title(self, title: str) -> List[TaskHeader]:
        return [
            TaskHeader.to_task_header(t)
            for t in self.fetch()
            if title.lower() in t.title.lower()
        ]

    def fetch_by_status(self, status: str) -> List[TaskHeader]:
        return [
            TaskHeader.to_task_header(t)
            for t in self.fetch()
            if status.upper() == t.status.upper()
        ]

    def delete(self, task_id: str) -> None:
        tasks = self.fetch()
        initial_count = len(tasks)
        tasks = [t for t in tasks if t.task_id != task_id]

        if len(tasks) == initial_count:
            raise ExceptionDriven(
                self._fs.driving_component,
                [self._fs.error_builder.entity_not_exists("task_id", task_id)],
            )

        self._write_all(tasks)
        self.create_views(tasks)
        return None

    def fetch(self) -> List[Task]:
        data = self._fs.read()
        if not isinstance(data, list):
            return []

        tasks = []
        for t in data:
            if "user_audit" in t and isinstance(t["user_audit"], dict):
                t["user_audit"] = Audit(**t["user_audit"])
            tasks.append(Task(**t))
        return tasks

    def create_views(self, tasks: List[Task]):
        self._create_view_by_tag(tasks)
        self._create_view_by_sub_task(tasks)
        return None

    def _write_all(self, tasks: List[Task]):
        sorted_tasks = sorted(tasks, key=lambda x: x.task_id, reverse=True)
        data = [t.as_dict() for t in sorted_tasks]
        self._fs.write(data)

    def _create_view_by_tag(self, tasks: List[Task]):
        view_by_tag = {}
        for task in tasks:
            for tag in task.task_tags:
                if tag not in view_by_tag:
                    view_by_tag[tag] = []
                view_by_tag[tag].append(task.task_id)

        view_path = self._fs.path.parent / f"{self.view_tag_table}.json"
        sorted_view_by_tag = dict(sorted(view_by_tag.items()))
        self._fs.write_external(sorted_view_by_tag, view_path)
        return None

    def _create_view_by_sub_task(self, tasks: List[Task]):
        view_by_parent = {}
        for task in tasks:
            parents = task.linked_items.get(TaskLinkedKey.TASK_PARENT, [])
            for parent_id in parents:
                if parent_id not in view_by_parent:
                    view_by_parent[parent_id] = []
                view_by_parent[parent_id].append(task.task_id)

        view_path = self._fs.path.parent / f"{self.view_sub_task_table}.json"
        sorted_view = dict(sorted(view_by_parent.items()))
        self._fs.write_external(sorted_view, view_path)
        return None
