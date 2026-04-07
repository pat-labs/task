import json
from typing import Dict

from src.domain.constants.Constants import Constants
from src.domain.enum.TaskStatus import TaskStatus
from src.domain.identifier.Identifier import Identifier
from src.domain.model.ModelAudit import ModelAudit
from src.domain.model.task.ModelTask import ModelTask


class MapperTask:
    @staticmethod
    def args_to_model(title: str, user_wrote_id: str):
        now = Identifier.get_datetime_identifier(Constants.DATE_TIME_FORMAT)
        audit = ModelAudit(
            user_wrote_id=user_wrote_id,
            updated_at=now,
            user_created_id=user_wrote_id,
            created_at=now,
        )
        return ModelTask(
            task_id=ModelTask.get_identifier(),
            title=title,
            detail=[],
            status=TaskStatus.OPEN.name,
            linked_items={},
            task_tags=[],
            user_assigned_id=user_wrote_id,
            user_audit=audit._asdict(),
        )

    @staticmethod
    def str_to_model(json_data: str):
        data = json.loads(json_data)
        return MapperTask.dict_to_model(data)

    @staticmethod
    def dict_to_model(data: Dict) -> ModelTask:
        audit_data = data["user_audit"]
        audit = ModelAudit(
            user_wrote_id=audit_data["user_wrote_id"],
            updated_at=audit_data["updated_at"],
            user_created_id=audit_data["user_created_id"],
            created_at=audit_data["created_at"],
        )
        return ModelTask(
            task_id=data["task_id"],
            title=data["title"],
            detail=data["detail"],
            status=data["status"],
            linked_items=data["linked_items"],
            task_tags=data["task_tags"],
            user_assigned_id=audit_data["user_wrote_id"],
            user_audit=audit._asdict(),
        )
