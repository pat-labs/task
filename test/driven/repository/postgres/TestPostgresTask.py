import unittest
from test.driven.repository.postgres.TestMyPostgres import TestMyPostgres
from test.driven.repository.TestRepositoryTask import TestRepositoryTask

from src.driven.repository.postgres.PostgresTask import PostgresTask
from src.driving.config.BuilderLogger import BuilderLogger


class TestPostgresTask(TestMyPostgres, TestRepositoryTask):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        logger = (
            BuilderLogger(cls.env.log_level, cls.env.log_dir, cls.env.log_to_console)
            .build()
            .get_logger("app")
        )
        if cls.db:
            cls.repository = PostgresTask(cls.db, logger)

    def setUp(self):
        super().setUp()
        if self.repository:
            self.repository.setup_database()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


if __name__ == "__main__":
    unittest.main()
