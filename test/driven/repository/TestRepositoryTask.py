from src.domain.dto.DtoTaskBase import DtoTaskBase
from src.driven.repository.Identifier.MySnowflake import MySnowflake


class TestRepositoryTask:
    repository = None

    def test_crud_lifecycle(self):
        # --- SETUP: Generate IDs and Task ---
        identifier = MySnowflake.generate()
        task = DtoTaskBase.to_task(identifier, "Initial CRUD Task", "0007")
        task = task._replace(
            task_linked_items=[["TASK_RELATED", "260427191736"]],
            task_tags=["WORK", "URGENT"],
            status="OPEN",
        )

        # 1. CREATE
        self.repository.create(task)

        # 2. VERIFY EXISTENCE (Check Boolean)
        self.assertTrue(self.repository.entity_exists(task.task_id))
        self.assertFalse(self.repository.entity_exists("invalid_id_999"))

        # 3. FETCH HEADERS (Verify Listing)
        headers = self.repository.fetch_headers_tasks()
        self.assertTrue(any(h.task_id == task.task_id for h in headers))

        # 4. FETCH BY TAG
        urgent_tasks = self.repository.fetch_by_tag("WORK")
        self.assertTrue(any(t.task_id == task.task_id for t in urgent_tasks))

        non_existent_tags = self.repository.fetch_by_tag("ghost-tag")
        self.assertFalse(any(t.task_id == task.task_id for t in non_existent_tags))

        # 5. FETCH BY STATUS
        todo_tasks = self.repository.fetch_by_status("OPEN")
        self.assertTrue(any(t.task_id == task.task_id for t in todo_tasks))

        # 6. UPDATE
        updated_title = "Updated Lifecycle Task"
        updated_task = task._replace(title=updated_title, status="DONE")
        self.repository.update(updated_task)

        # 7. FETCH BY ID & VERIFY UPDATE
        fetched = self.repository.fetch_by_id(task.task_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.title, updated_title)
        self.assertEqual(fetched.status, "DONE")

        # 8. FETCH BY TITLE (Search)
        searched = self.repository.fetch_by_title("Lifecycle Task")
        self.assertTrue(any(t.task_id == task.task_id for t in searched))

        # 9. DELETE
        self.repository.delete(task.task_id)

        # 10. VERIFY DELETION
        self.assertFalse(self.repository.entity_exists(task.task_id))
        deleted_fetched = self.repository.fetch_by_id(task.task_id)
        self.assertIsNone(deleted_fetched)
