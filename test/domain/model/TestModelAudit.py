from src.domain.model.ModelAudit import ModelAudit


class TestModelAudit:
    @staticmethod
    def get_model() -> ModelAudit:
        return ModelAudit(
            audit_id="007",
            user_wrote_id="007",
            updated_at="20260101000000",
            user_created_id="001",
            created_at="20260101000000",
        )
