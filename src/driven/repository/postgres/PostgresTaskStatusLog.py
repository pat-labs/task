from src.domain.constants.Constants import Constants
from src.domain.constants.ConstantsTask import ConstantsTask
from src.domain.model.StatusLog import StatusLog
from src.driven.repository.postgres.MyPostgres import MyPostgres


class PostgresTaskStatusLog:
    def __init__(self, my_postgres: MyPostgres) -> None:
        self._db = my_postgres
        self.console_log = my_postgres.console_log

    def setup_database(self) -> None:
        with self._db.get_cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS tasks_status_log CASCADE")

            create_tasks_log_status = f"""
                CREATE TABLE IF NOT EXISTS tasks_status_log(
                task_id VARCHAR({ConstantsTask.TASK_ID_MAX_SIZE}) REFERENCES tasks(task_id) ON DELETE CASCADE,
                status VARCHAR({ConstantsTask.TASK_STATUS_MAX_SIZE}),
                user_wrote_id VARCHAR({Constants.USER_ID_MAX_SIZE}),
                wrote_at VARCHAR({Constants.DATE_TIME_FORMAT_MAX_SIZE})
                );
            """
            cursor.execute(create_tasks_log_status)
            self.console_log.debug(cursor.query.decode("utf-8"))

    def create(self, status_log: StatusLog):
        with self._db.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks_status_log (
                    task_id,
                    status,
                    user_wrote_id,
                    wrote_at)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    status_log.task_id,
                    status_log.status,
                    status_log.user_wrote_id,
                    status_log.wrote_at,
                ),
            )
            self.console_log.debug(cursor.query.decode("utf-8"))

    def delete(self, task_id: str):
        with self._db.get_cursor() as cursor:
            cursor.execute(
                """
                DELETE
                FROM tasks_status_log
                WHERE task_id = %s
                """,
                (task_id,),
            )
            self.console_log.debug(cursor.query.decode("utf-8"))
