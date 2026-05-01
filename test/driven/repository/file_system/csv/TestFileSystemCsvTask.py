import unittest
from pathlib import Path
from test.driven.repository.TestRepositoryTask import TestRepositoryTask

from src.driven.repository.file_system.csv.FileSystemCsvTask import \
    FileSystemCsvTask
from src.driven.repository.file_system.MyFileSystemCsv import MyFileSystemCsv
from src.driving.config.BuilderLogger import BuilderLogger


class TestFileSystemCsvTask(unittest.TestCase, TestRepositoryTask):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path("./tmp")

        logger = BuilderLogger("DEBUG", "log", True).build().get_logger("test")

        cls.fs = MyFileSystemCsv(str(cls.test_dir))
        cls.repository = FileSystemCsvTask(cls.fs, logger)
        cls.repository.setup_database()


if __name__ == "__main__":
    unittest.main()
