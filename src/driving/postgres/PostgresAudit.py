from src.domain.constants.Constants import Constants
from src.driven.repository.dao.DaoAudit import DaoAudit
from src.driving.postgres.MyPostgres import MyPostgres


class PostgresAudit:
    def __init__(self, my_postgres: MyPostgres) -> None:
        self._db = my_postgres

    def setup_database(self) -> None:
        with self._db.get_cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS audit")

            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS audit (
                    audit_id VARCHAR({Constants.USER_ID_MAX_SIZE}),
                    user_wrote_id VARCHAR({Constants.USER_ID_MAX_SIZE}),
                    updated_at VARCHAR({Constants.DATE_TIME_FORMAT_MAX_SIZE}),
                    user_created_id VARCHAR({Constants.USER_ID_MAX_SIZE}),
                    created_at VARCHAR({Constants.DATE_TIME_FORMAT_MAX_SIZE})
                );
                """)

    def create(self, dao_audit: DaoAudit) -> None:
        with self._db.get_cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO audit (
                    audit_id,
                    user_wrote_id,
                    updated_at,
                    user_created_id,
                    created_at
                )
                VALUES (%s, %s, TO_TIMESTAMP(%s, {Constants.DATE_TIME_FORMAT}), %s, TO_TIMESTAMP(%s, {Constants.DATE_TIME_FORMAT}))
                """,
                (
                    dao_audit.audit_id,
                    dao_audit.user_wrote_id,
                    dao_audit.updated_at,
                    dao_audit.user_created_id,
                    dao_audit.created_at,
                ),
            )

    def is_not_valid_user_id(self, user_id: str) -> None:
        return None
