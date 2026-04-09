import json
from typing import Dict

from src.domain.enum.TaskStatus import TaskStatus
from src.domain.model.Audit import Audit
from src.domain.model.task.Task import Task


class MapperTask:
    @staticmethod
    def args_to_model(title: str, user_wrote_id: str) -> Task:
        audit = Audit.create(
            user_wrote_id=user_wrote_id,
        )
        return Task(
            task_id=Task.get_identifier(),
            title=title,
            detail=[],
            status=TaskStatus.OPEN.name,
            linked_items={},
            task_tags=[],
            user_assigned_id=user_wrote_id,
            user_audit=audit,
        )

    @staticmethod
    def str_to_model(json_data: str) -> Task:
        data = json.loads(json_data)
        return MapperTask.dict_to_model(data)

    @staticmethod
    def dict_to_model(data: Dict) -> Task:
        audit_data = data.get("user_audit", {})

        audit = Audit(
            user_wrote_id=audit_data.get("user_wrote_id", ""),
            updated_at=audit_data.get("updated_at", ""),
            user_created_id=audit_data.get("user_created_id", ""),
            created_at=audit_data.get("created_at", ""),
        )

        return Task(
            task_id=data.get("task_id", Task.get_identifier()),
            title=data.get("title", ""),
            detail=data.get("detail", []),
            status=data.get("status", TaskStatus.OPEN.name),
            linked_items=data.get("linked_items", {}),
            task_tags=data.get("task_tags", []),
            user_assigned_id=data.get("user_assigned_id", audit.user_wrote_id),
            user_audit=audit,
        )
