import unittest

from src.driven.repository.Identifier.MySnowflake import MySnowflake


class TestMySnowflake(unittest.TestCase):

    def test_generate_sync_returns_string(self):
        snowflake_id = MySnowflake.generate()

        self.assertIsInstance(snowflake_id, str)
        self.assertTrue(len(snowflake_id) > 0)
        self.assertTrue(snowflake_id.isdigit())

    def test_generate_uniqueness(self):
        ids = set()
        count = 100
        for _ in range(count):
            ids.add(MySnowflake.generate())

        self.assertEqual(len(ids), count)

    def test_id_ordering(self):
        id1 = MySnowflake.generate()
        id2 = MySnowflake.generate()
        id3 = MySnowflake.generate()

        self.assertLess(int(id1), int(id2))
        self.assertLess(int(id2), int(id3))

    def test_static_access(self):
        try:
            MySnowflake.generate()
        except TypeError:
            self.fail(
                "MySnowflake.generate() raised TypeError (likely not a staticmethod)"
            )
