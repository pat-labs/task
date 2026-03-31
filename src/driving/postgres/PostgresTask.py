from typing import List

from src.domain.constants.Constants import Constants
from src.domain.constants.ConstantsTask import (
    ConstantsTask,
    ConstantsTaskLabel,
    ConstantsTaskStatus,
)
from src.domain.dto.DtoFetchHeadersTasks import DtoFetchHeadersTasks
from src.domain.model.ModelTask import ModelTask
from src.driving.postgres.AuditUtil import AuditUtil
from src.driving.postgres.MyPostgres import MyPostgres


class PostgresTask:
    def __init__(self, my_postgres: MyPostgres) -> None:
        self._db = my_postgres

    def setup_database(self) -> None:
        with self._db.get_cursor() as cursor:
            cursor.execute("DROP MATERIALIZED VIEW IF EXISTS mv_task")

            cursor.execute("DROP TABLE IF EXISTS task_status")
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS task_status (
                    task_status_id VARCHAR({ConstantsTaskStatus.TASK_STATUS_ID_MAX_SIZE}) PRIMARY KEY,
                    detail VARCHAR({ConstantsTaskStatus.TASK_STATUS_DESCRIPTION_MAX_SIZE})
                );
                """)

            cursor.execute("DROP TABLE IF EXISTS task_tag")
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS task_tag (
                    task_tag_id VARCHAR({ConstantsTaskLabel.TASK_TAG_ID_MAX_SIZE}) PRIMARY KEY,
                    detail VARCHAR({ConstantsTaskLabel.TASK_TAG_DESCRIPTION_MAX_SIZE})
                );
                """)

            cursor.execute("DROP TABLE IF EXISTS task")
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS task (
                    task_id VARCHAR({ConstantsTask.TASK_ID_MAX_SIZE}) PRIMARY KEY,
                    tittle VARCHAR({ConstantsTask.TASK_TITTLE_MAX_SIZE}),
                    detail VARCHAR({ConstantsTask.TASK_DESCRIPTION_MAX_SIZE}),
                    status VARCHAR({ConstantsTask.TASK_STATUS_MAX_SIZE}),
                    task_ids VARCHAR({ConstantsTask.TASK_ID_MAX_SIZE}),
                    task_tags TEXT[],
                    user_assigned_id VARCHAR({Constants.USER_ID_MAX_SIZE}),
                    {AuditUtil.get_sql_query()}
                );
                """)

            cursor.execute("""
                CREATE MATERIALIZED VIEW IF NOT EXISTS mv_task AS
                SELECT
                    task_id,
                    tittle,
                    task_tags,
                    status,
                    user_assigned_id
                FROM task
                WHERE status = 0;
                """)

            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_task_task_id
                    ON mv_task (task_id);
                """)

    def create(self, model_task: ModelTask) -> None:
        with self._db.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO task (task_id,
                                  tittle,
                                  detail,
                                  status,
                                  task_ids,
                                  task_tags,
                                  user_assigned_id,
                                  user_audit_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    model_task.task_id,
                    model_task.tittle,
                    model_task.detail,
                    model_task.status,
                    model_task.task_ids,
                    model_task.task_tags,
                    model_task.user_assigned_id,
                    model_task.user_audit,
                ),
            )

            cursor.execute("""
                REFRESH MATERIALIZED VIEW mv_task
                """)

    def fetch_headers_tasks(self) -> List[DtoFetchHeadersTasks]:
        with self._db.get_cursor() as cursor:
            cursor.execute("""
                SELECT task_id,
                       tittle,
                       task_tags,
                       status,
                       user_assigned_id
                FROM mv_task
                """)
            rows = cursor.fetchall()

        tasks = [
            DtoFetchHeadersTasks(
                task_id=row[0],
                tittle=row[1],
                task_tags=row[2],
                status=row[3],
                user_assigned_id=row[4],
            )
            for row in rows
        ]

        return tasks

    def delete(self, task_id: str):
        with self._db.get_cursor() as cursor:
            cursor.execute(
                """
                DELETE
                FROM task
                WHERE task_id = %s
                """,
                (task_id,),
            )

            cursor.execute("""
                REFRESH MATERIALIZED VIEW mv_task
                """)

    def update(self, model_task: ModelTask):
        with self._db.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE task
                SET user_assigned_id = %s,
                    detail           = %s,
                    status           = %s,
                    task_tags        = %s,
                    WHERE task_id = %s
                """,
                (
                    model_task.user_assigned_id,
                    model_task.detail,
                    model_task.status,
                    model_task.task_tags,
                    model_task.task_id,
                ),
            )
