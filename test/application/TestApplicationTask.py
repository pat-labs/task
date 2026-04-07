import os
import shutil
import unittest
from time import sleep
from typing import List

from src.domain.dto.DtoFetchHeadersTasks import DtoFetchHeadersTasks
from src.domain.mapper.MapperTask import MapperTask
from src.domain.model.ModelTask import ModelTask
from src.driven.application.ApplicationTask import ApplicationTask
from src.driving.config.Bootstrap import Bootstrap
from src.driving.fyle_system.FileSystemTask import FileSystemTask
from src.driving.fyle_system.MyFileSystem import MyFileSystem

base_dir = os.path.dirname(os.path.abspath(__file__))


class TestApplicationTask(unittest.TestCase):
    def setUp(self) -> None:
        bootstrap = Bootstrap.load_bootstrap()
        self.task = ModelTask.get_template()

        self.db_path = os.path.join(bootstrap.project_dir, "db")
        repository = MyFileSystem(self.db_path)
        repository_task = FileSystemTask(repository)
        self.application_task = ApplicationTask(repository_task)

    def tearDown(self) -> None:
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)

    def test_happy_path(self):
        # 1.1. Create a task
        new_task_template = ModelTask.get_template()._asdict()
        new_task_template.update(self.task._asdict())
        task = MapperTask.dict_to_model(new_task_template)
        self.application_task.create(task)

        # 1.2. Use base create
        sleep(1)
        base_task = MapperTask.args_to_model("test 2", "001")
        self.application_task.create(base_task)

        # 2. Fetch headers and verify
        headers_tasks = self.application_task.fetch_headers()
        self.assertEqual(len(headers_tasks), 2)
        task_id = headers_tasks[0].task_id

        # 3. Update the task
        task_to_update = self.application_task.fetch_by_id(task_id)
        self.assertIsNotNone(task_to_update)

        updated_task = task_to_update._replace(title="Updated Task")
        self.application_task.update(updated_task)

        # 4. Verify update
        refetched_task = self.application_task.fetch_by_id(task_id)
        self.assertEqual(refetched_task.title, "Updated Task")

        # 5. Delete the task
        self.application_task.delete(task_id)

        # 6. Verify deletion
        all_tasks = self.application_task.fetch()
        self.assertEqual(len(all_tasks), 1)
        self.assertIsNone(self.application_task.fetch_by_id(task_id))


if __name__ == "__main__":
    unittest.main()
