from typing import List

from src.domain.constants.ConstantsTask import ConstantsTask
from src.domain.model.LinkedItem import LinkedItem
from src.driven.repository.postgres.MyPostgres import MyPostgres


class PostgresTaskLinkedItem:
    def __init__(self, my_postgres: MyPostgres) -> None:
        self._db = my_postgres
        self.console_log = my_postgres.console_log

    def setup_database(self) -> None:
        with self._db.get_cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS task_linked_items CASCADE")

            create_tasks_tags = f"""
                CREATE TABLE task_linked_items (
                task_id VARCHAR({ConstantsTask.TASK_ID_MAX_SIZE}) REFERENCES tasks(task_id) ON DELETE CASCADE,
                linked_key VARCHAR({ConstantsTask.TASK_LINKED_ITEM_KEY_MAX_SIZE}),
                linked_value VARCHAR({ConstantsTask.TASK_LINKED_ITEM_DESCRIPTION_MAX_SIZE}),
                PRIMARY KEY (task_id, linked_key, linked_value)
            );
            """
            cursor.execute(create_tasks_tags)
            self.console_log.debug(cursor.query.decode("utf-8"))

    def create(self, linked_items: List[LinkedItem]):
        with self._db.get_cursor() as cursor:
            for item in linked_items:
                cursor.execute(
                    """
                        INSERT INTO task_linked_items (
                        task_id,
                        linked_key,
                        linked_value)
                        VALUES (%s, %s, %s)
                    """,
                    (item.task_id, item.linked_key, item.linked_value),
                )
                self.console_log.debug(cursor.query.decode("utf-8"))

    def fetch_by_id(self, task_id: str) -> List[LinkedItem]:
        with self._db.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id,
                linked_key,
                linked_value
                FROM task_linked_items
                WHERE task_id = %s
                ORDER BY linked_key DESC
                """,
                (task_id,),
            )
            self.console_log.debug(cursor.query.decode("utf-8"))
            rows = cursor.fetchall()

        if not rows:
            return []

        return rows

    def delete(self, task_id: str):
        with self._db.get_cursor() as cursor:
            cursor.execute(
                """
                DELETE
                FROM task_linked_items
                WHERE task_id = %s
                """,
                (task_id,),
            )
            self.console_log.debug(cursor.query.decode("utf-8"))

    def update(self, linked_items: List[LinkedItem]):
        if linked_items:
            self.delete(linked_items[0].task_id)
            self.create(linked_items=linked_items)
