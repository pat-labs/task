from typing import List, Optional

from src.domain.constants.Constants import Constants
from src.domain.constants.ConstantsTask import ConstantsTask
from src.domain.dto.DtoTaskHeader import DtoTaskHeader
from src.domain.model.Audit import Audit
from src.domain.model.Task import Task
from src.driven.repository.postgres.MyPostgres import MyPostgres
from src.driven.repository.postgres.PostgresTaskLinkedItem import \
    PostgresTaskLinkedItem
from src.driven.repository.postgres.PostgresTaskStatusLog import \
    PostgresTaskStatusLog


class PostgresTask:
    def __init__(self, my_postgres: MyPostgres) -> None:
        self._db_task = my_postgres
        self.console_log = my_postgres.console_log

        self._db_linked_items = PostgresTaskLinkedItem(my_postgres)
        self._db_status_log = PostgresTaskStatusLog(my_postgres)

    @staticmethod
    def get_setup_audit():
        return f"""
            user_wrote_id VARCHAR({Constants.USER_ID_MAX_SIZE}),
            updated_at VARCHAR({Constants.DATE_TIME_FORMAT_MAX_SIZE}),
            user_created_id VARCHAR({Constants.USER_ID_MAX_SIZE}),
            created_at VARCHAR({Constants.DATE_TIME_FORMAT_MAX_SIZE})
        """

    def setup_database(self) -> None:
        with self._db_task.get_cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS tasks CASCADE")

            create_task_query = f"""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id VARCHAR({ConstantsTask.TASK_ID_MAX_SIZE}) PRIMARY KEY,
                    title VARCHAR({ConstantsTask.TASK_TITLE_MAX_SIZE}),
                    status VARCHAR({ConstantsTask.TASK_STATUS_MAX_SIZE}),
                    task_tags TEXT[],
                    user_assigned_id VARCHAR({Constants.USER_ID_MAX_SIZE}),
                    {PostgresTask.get_setup_audit()}
                );
                """
            cursor.execute(create_task_query)
            self.console_log.debug(cursor.query.decode("utf-8"))

        self._db_linked_items.setup_database()
        self._db_status_log.setup_database()

        self.console_log.info("Database setup successfully.")

    # -------------------------
    # Write
    # -------------------------

    def create(self, task: Task) -> None:
        print(task._asdict())
        audit = Audit.from_dict(task.user_audit)

        with self._db_task.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks (
                    task_id,
                    title,
                    status,
                    task_tags,
                    user_assigned_id,
                    user_wrote_id,
                    updated_at,
                    user_created_id,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    task.task_id,
                    task.title,
                    task.status,
                    task.task_tags,
                    task.user_assigned_id,
                    audit.user_wrote_id,
                    audit.updated_at,
                    audit.user_created_id,
                    audit.created_at,
                ),
            )
            self.console_log.debug(cursor.query.decode("utf-8"))

        linked_items = task.get_linked_items()
        if linked_items:
            self._db_linked_items.create(linked_items)

        status_log = task.get_status_log()
        self._db_status_log.create(status_log)

    def delete(self, task_id: str) -> None:
        with self._db_task.get_cursor() as cursor:
            cursor.execute(
                """
                DELETE
                FROM tasks
                WHERE task_id = %s
                """,
                (task_id,),
            )
            self.console_log.debug(cursor.query.decode("utf-8"))
        return None

    def update(self, task: Task) -> None:
        with self._db_task.get_cursor() as cursor:
            audit = Audit.from_dict(task.user_audit)

            cursor.execute(
                """
                UPDATE tasks
                SET title            = %s,
                    status           = %s,
                    task_tags        = %s,
                    user_assigned_id = %s,
                    user_wrote_id    = %s,
                    updated_at       = %s
                WHERE task_id = %s
                """,
                (
                    task.title,
                    task.status,
                    task.task_tags,
                    task.user_assigned_id,
                    audit.user_wrote_id,
                    audit.updated_at,
                    task.task_id,
                ),
            )
            self.console_log.debug(cursor.query.decode("utf-8"))

        linked_items = task.get_linked_items()
        if linked_items:
            self._db_linked_items.update(linked_items)

        status_log = task.get_status_log()
        self._db_status_log.create(status_log)

        return None

    # -------------------------
    # Read
    # -------------------------

    def entity_exists(self, task_id: str) -> bool:
        with self._db_task.get_cursor() as cursor:
            cursor.execute("SELECT 1 FROM tasks WHERE task_id = %s", (task_id,))
            self.console_log.debug(cursor.query.decode("utf-8"))
            return cursor.fetchone() is not None

    def fetch_headers_tasks(self) -> List[DtoTaskHeader]:
        with self._db_task.get_cursor() as cursor:
            cursor.execute("""
                           SELECT task_id,
                                  title,
                                  task_tags,
                                  status,
                                  user_assigned_id
                           FROM tasks
                           """)
            self.console_log.debug(cursor.query.decode("utf-8"))
            rows = cursor.fetchall()

        tasks = [DtoTaskHeader.from_list(row) for row in rows]

        return tasks

    def fetch(self) -> List[Task]:
        with self._db_task.get_cursor() as cursor:
            cursor.execute("""
                SELECT task_id, title, status, task_tags,
                user_assigned_id, user_wrote_id, updated_at, user_created_id, created_at
                FROM tasks
                ORDER BY task_id DESC
                """)
            self.console_log.debug(cursor.query.decode("utf-8"))
            rows = cursor.fetchall()

        tasks = []
        for row_tuple in rows:
            row_list = list(row_tuple)
            linked_items = self._db_linked_items.fetch_by_id(row_list[0])
            row_list.insert(3, linked_items)
            tasks.append(Task.from_list(row_list))
        return tasks

    def fetch_by_id(self, task_id: str) -> Optional[Task]:
        with self._db_task.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id, title, status, task_tags,
                user_assigned_id, user_wrote_id, updated_at, user_created_id, created_at
                FROM tasks
                WHERE task_id = %s
                """,
                (task_id,),
            )
            self.console_log.debug(cursor.query.decode("utf-8"))
            row_tuple = cursor.fetchone()  # Renamed to avoid confusion

        if not row_tuple:
            return None

        linked_items_data = self._db_linked_items.fetch_by_id(task_id)
        linked_items = list(linked_items_data)

        row_list = list(row_tuple)
        row_list.insert(3, linked_items)

        return Task.from_list(row_list)

    def fetch_by_ids(self, task_ids: List[str]) -> List[DtoTaskHeader]:
        if not task_ids:
            return []
        with self._db_task.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id, title, task_tags, status, user_assigned_id
                FROM tasks
                WHERE task_id = ANY(%s)
                """,
                (task_ids,),
            )
            self.console_log.debug(cursor.query.decode("utf-8"))
            rows = cursor.fetchall()

        return [DtoTaskHeader.from_list(row) for row in rows]

    def fetch_by_tag(self, tag: str) -> List[DtoTaskHeader]:
        with self._db_task.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id, title, task_tags, status, user_assigned_id
                FROM tasks
                WHERE %s = ANY(task_tags)
                """,
                (tag,),
            )
            self.console_log.debug(cursor.query.decode("utf-8"))
            rows = cursor.fetchall()

        return [DtoTaskHeader.from_list(row) for row in rows]

    def fetch_by_title(self, title: str) -> List[DtoTaskHeader]:
        with self._db_task.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id, title, task_tags, status, user_assigned_id
                FROM tasks
                WHERE title ILIKE %s
                """,
                (f"%{title}%",),
            )
            self.console_log.debug(cursor.query.decode("utf-8"))
            rows = cursor.fetchall()

        return [DtoTaskHeader.from_list(row) for row in rows]

    def fetch_by_status(self, status: str) -> List[DtoTaskHeader]:
        with self._db_task.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id, title, task_tags, status, user_assigned_id
                FROM tasks
                WHERE status ILIKE %s
                """,
                (status,),
            )
            self.console_log.debug(cursor.query.decode("utf-8"))
            rows = cursor.fetchall()

        return [DtoTaskHeader.from_list(row) for row in rows]
