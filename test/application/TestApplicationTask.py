import os
import unittest
from test.domain.model.TestModelTask import TestModelTask
from typing import List

from src.domain.dto.DtoFetchHeadersTasks import DtoFetchHeadersTasks
from src.domain.mapper.MapperTask import MapperTask
from src.domain.model.ModelTask import ModelTask
from src.driven.application.ApplicationTask import ApplicationTask

base_dir = os.path.dirname(os.path.abspath(__file__))


class MockRepositoryTask:
    def validate(self, task: ModelTask) -> List[str]:
        return []

    def create(self, task: ModelTask):
        return None

    def fetch_headers_tasks(self) -> List[DtoFetchHeadersTasks]:
        return TestModelTask.fetch_headers_tasks()

    def update(self, task: ModelTask):
        return None

    def fetch_by_id(self, task_id: str) -> Optional[ModelTask]:
        return TestModelTask.get_model()

    def delete(self, task_id: str):
        return None

    def fetch(self) -> List[ModelTask]:
        return TestModelTask.fetch()


class TestApplicationTask(unittest.TestCase):
    def setUp(self) -> None:
        self.task = TestModelTask.get_model()

        repository_task = MockRepositoryTask()
        self.application_task = ApplicationTask(repository_task)

    def test_happy_path(self):
        new_task_template = ModelTask.get_template()._asdict()
        new_task_template.update(self.task._asdict())
        task = MapperTask.to_model(new_task_template)
        self.assertIsNone(self.application_task.create(task))
        tasks = self.application_task.fetch_headers_tasks()
        self.assertEqual(len(tasks), 1)

        old_task_template = ModelTask.empty_model()._asdict()
        old_task = tasks[0]
        old_task.tittle = "Updated Task"
        old_task_template.update(old_task._asdict())
        self.application_task.update(old_task_template)
        self.application_task.fetch_by_id(old_task.task_id)

        task_id_to_delete = tasks[0].task_id
        self.application_task.delete(task_id_to_delete)
        self.application_task.fetch()




if __name__ == "__main__":
    unittest.main()
