import json
import os
import unittest

from src.domain.dto.DtoNewAudit import DtoNewAudit
from src.domain.dto.DtoNewTask import DtoNewTask
from src.driven.application.ApplicationAudit import ApplicationAudit
from src.driven.application.ApplicationTask import ApplicationTask
from src.driven.repository.dao.DaoAudit import DaoAudit
from src.driven.repository.dao.DaoTask import ModelTask
from src.driving.postgres.MyPostgres import MyPostgres
from src.driving.postgres.PostgresAudit import PostgresAudit
from src.driving.postgres.PostgresTask import PostgresTask

base_dir = os.path.dirname(os.path.abspath(__file__))


class MockRepositoryTask:
    def __init__(self):
        dao_task_path = os.path.join(base_dir, "../../resource/dao/Task.json")
        with open(dao_task_path, "r") as file:
            self.dao_task_data = json.load(file)

    def create(self, dao_task):
        first_item = self.dao_task_data[0]
        return ModelTask(
            first_item["task_id"],
            first_item["user_assigned_id"],
            first_item["detail"],
            first_item["milestones"],
            first_item["status"],
            first_item["task_tags"],
            first_item["user_audit_id"],
        )


class MockRepositoryAudit:
    def __init__(self):
        dao_audit_path = os.path.join(base_dir, "../../resource/dao/Audit.json")
        with open(dao_audit_path, "r") as file:
            self.dao_audit_data = json.load(file)

    def create(self, dao_audit):
        return DaoAudit(
            self.dao_audit_data["audit_id"],
            self.dao_audit_data["user_wrote_id"],
            self.dao_audit_data["updated_at"],
            self.dao_audit_data["user_created_id"],
            self.dao_audit_data["created_at"],
        )

    def is_not_valid_user_id(self, user_id: str) -> None:
        return None


class MockTask:
    @staticmethod
    def get_new_task():
        dto_task_path = os.path.join(base_dir, "../../resource/dao/Task.json")
        with open(dto_task_path, "r") as file:
            task_data = json.load(file)

        first_item = task_data[0]
        return DtoNewTask(
            task_id=first_item["task_id"],
            user_assigned_id=first_item["user_assigned_id"],
            description=first_item["detail"],
            milestones=first_item["milestones"],
        )


class MockAudit:
    @staticmethod
    def get_new_audit():
        dto_audit_path = os.path.join(base_dir, "../../resource/dao/Audit.json")
        with open(dto_audit_path, "r") as file:
            audit_data = json.load(file)

        return DtoNewAudit(user_created_id=audit_data["user_created_id"])


class TestTask(unittest.TestCase):

    def setUp(self):
        self.postgres = MyPostgres(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            database=os.getenv("POSTGRES_DB", "task"),
            port=int(os.getenv("POSTGRES_PORT", 5432)),
        )

        self.repository_task = PostgresTask(self.postgres)
        self.repository_audit = PostgresAudit(self.postgres)

        self.repository_task.setup_database()
        self.repository_audit.setup_database()

        self.task_data = MockTask.get_new_task()
        self.audit_data = MockAudit.get_new_audit()

        self.application_task = ApplicationTask(self.repository_task)
        self.application_audit = ApplicationAudit(self.repository_audit)

    def tearDown(self):
        self.postgres.close()

    def test_new_task(self):
        dao_audit = self.application_audit.create(self.audit_data)
        dao_task = self.application_task.create(self.task_data, dao_audit)

        self.assertEqual(dao_task.task_id, self.task_data.task_id)
        self.assertEqual(dao_task.description, self.task_data.description)
        self.assertEqual(dao_task.milestones, self.task_data.milestones)

    def test_fetch_tasks(self):
        tasks = self.application_task.fetch_headers()
        self.assertEqual(len(tasks), 1)


if __name__ == "__main__":
    unittest.main()
