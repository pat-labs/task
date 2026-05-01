import csv
import shutil
import unittest
from pathlib import Path

from src.driven.repository.file_system.MyFileSystemCsv import MyFileSystemCsv


class TestMyFileSystem(unittest.TestCase):
    def setUp(self):
        self.base_path = Path("./tmp")
        self.base_path.mkdir(exist_ok=True, parents=True)
        self.file_system = MyFileSystemCsv(str(self.base_path))

    def tearDown(self):
        if self.base_path.exists():
            shutil.rmtree(self.base_path)

    def test_build_path(self):
        path = self.file_system.build_path(schema="test_schema", table="test_table")
        expected_path = self.base_path / "test_schema" / "test_table.csv"
        self.assertEqual(path, expected_path)
        self.assertTrue(expected_path.parent.exists())

    def test_write_and_read_csv(self):
        path = self.file_system.build_path(schema="csv_data", table="items")
        data_to_write = [
            {"id": "1", "name": "Item A", "value": "100"},
            {"id": "2", "name": "Item B", "value": "200"},
        ]
        self.file_system.write(path, data_to_write)

        read_data = self.file_system.read(path)
        self.assertEqual(read_data, data_to_write)

    def test_read_non_existent_file(self):
        path = self.base_path / "non_existent" / "file.csv"
        read_data = self.file_system.read(path)
        self.assertEqual(read_data, [])

    def test_write_empty_data(self):
        path = self.file_system.build_path(schema="empty_data", table="test")
        self.file_system.write(path, [])

        self.assertTrue(path.exists())
        with open(path, "r") as f:
            content = f.read()
            self.assertEqual(content, "")

        read_data = self.file_system.read(path)
        self.assertEqual(read_data, [])

    def test_create_with_headers(self):
        path = self.file_system.build_path(schema="headers", table="test")
        headers = ["id", "name", "value"]
        self.file_system.create_with_headers(path, headers)

        self.assertTrue(path.exists())
        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=self.file_system.separator)
            self.assertEqual(next(reader), headers)

    def test_write_append(self):
        path = self.file_system.build_path(schema="append", table="test")
        data1 = [{"id": "1", "name": "A"}]
        data2 = [{"id": "2", "name": "B"}]

        self.file_system.write(path, data1)
        self.file_system.write(path, data2, append=True)

        read_data = self.file_system.read(path)
        self.assertEqual(read_data, data1 + data2)

    def test_file_extension_can_be_changed(self):
        self.file_system.file_extension = ".txt"
        path = self.file_system.build_path(schema="custom_ext", table="my_file")
        expected_path = self.base_path / "custom_ext" / "my_file.txt"
        self.assertEqual(path, expected_path)

        self.file_system.file_extension = ".csv"


if __name__ == "__main__":
    unittest.main()
