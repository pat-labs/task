import unittest

from src.driven.repository.postgres.MyPostgres import MyPostgres
from src.driving.config.BuilderEnv import BuilderEnv


class TestMyPostgres(unittest.TestCase):
    db = None
    env = None

    @classmethod
    def setUpClass(cls):
        cls.env = BuilderEnv.load_env()
        try:
            cls.db = MyPostgres(
                host=cls.env.postgres_host,
                user=cls.env.postgres_user,
                password=cls.env.postgres_password,
                database=cls.env.postgres_db,
                port=cls.env.postgres_port,
            )
        except SystemExit:
            cls.db = None

    @classmethod
    def tearDownClass(cls):
        if cls.db:
            cls.db.close()

    def setUp(self):
        if self.db is None:
            self.skipTest("Database connection failed during setup class.")

    def test_connection_and_basic_query(self):
        result = self.db.fetch_one("SELECT 1")
        self.assertEqual(result[0], 1)

    def test_context_manager(self):
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT current_database()")
            db_name = cursor.fetchone()[0]
            self.assertEqual(db_name, self.env.postgres_db)


if __name__ == "__main__":
    unittest.main()
