from typing import Dict

from src.domain.model.ModelAudit import ModelAudit
from src.domain.model.ModelTask import ModelTask


class MapperTask:
    @staticmethod
    def to_model(data: Dict) -> ModelTask:
        audit_data = data["user_audit"]
        audit = ModelAudit(
            audit_id=audit_data["audit_id"],
            user_wrote_id=audit_data["user_wrote_id"],
            updated_at=audit_data["updated_at"],
            user_created_id=audit_data["user_created_id"],
            created_at=audit_data["created_at"],
        )
        return ModelTask(
            task_id=data["task_id"],
            tittle=data["tittle"],
            detail=data["detail"],
            status=data["status"],
            task_ids=data["task_ids"],
            task_tags=data["task_tags"],
            user_assigned_id=audit_data["user_wrote_id"],
            user_audit=audit._asdict(),
        )
