import unittest

from src.domain.enum.ErrorKey import ErrorKey
from src.domain.error.BuilderError import BuilderError
from src.domain.error.Error import Error


class TestBuilderError(unittest.TestCase):

    def test_required(self):
        error = BuilderError.required("task_id")
        self.assertIsInstance(error, Error)
        self.assertEqual(error.key, ErrorKey.REQUIRED)
        self.assertEqual(error.data, {"attr": "task_id"})

    def test_invalid_format(self):
        error = BuilderError.invalid_format("email", r"^[a-z]+$")
        self.assertEqual(error.key, ErrorKey.INVALID_FORMAT)
        self.assertEqual(error.data, {"attr": "email", "pattern": r"^[a-z]+$"})

    def test_invalid_value(self):
        error = BuilderError.invalid_value("status", "WRONG")
        self.assertEqual(error.key, ErrorKey.INVALID_VALUE)
        self.assertEqual(error.data, {"attr": "status", "value": "WRONG"})

    def test_max_size(self):
        error = BuilderError.max_size("title", 50)
        self.assertEqual(error.key, ErrorKey.MAX_SIZE)
        self.assertEqual(error.data, {"attr": "title", "max_size": 50})

    def test_not_unique_values(self):
        error = BuilderError.not_unique_values("tags")
        self.assertEqual(error.key, ErrorKey.NOT_UNIQUE_VALUES)
        self.assertEqual(error.data, {"attr": "tags"})

    def test_not_in_enum(self):
        values = ["OPEN", "CLOSED"]
        error = BuilderError.not_in_enum("status", values[0], values)
        self.assertEqual(error.key, ErrorKey.NOT_IN_ENUM)
        self.assertEqual(
            error.data, {"attr": "status", "value": values[0], "values": values}
        )

    def test_cast_fail(self):
        error = BuilderError.cast_fail("age", "int")
        self.assertEqual(error.key, ErrorKey.CAST_FAIL)
        self.assertEqual(error.data, {"attr": "age", "cls": "int"})

    def test_duplicate_key(self):
        error = BuilderError.duplicate_key("user_id", "007")
        self.assertEqual(error.key, ErrorKey.DUPLICATE_KEY)
        self.assertEqual(error.data, {"attr": "user_id", "value": "007"})

    def test_entity_not_exists(self):
        error = BuilderError.entity_not_exists("task_id", "123")
        self.assertEqual(error.key, ErrorKey.ENTITY_NOT_EXISTS)
        self.assertEqual(error.data, {"attr": "task_id", "value": "123"})

    def test_file_not_found(self):
        error = BuilderError.file_not_found("/tmp/test.json")
        self.assertEqual(error.key, ErrorKey.FILE_NOT_FOUND)
        self.assertEqual(error.data, {"path": "/tmp/test.json"})

    def test_invalid_json_format(self):
        error = BuilderError.invalid_json_format("test.json")
        self.assertEqual(error.key, ErrorKey.INVALID_JSON_FORMAT)
        self.assertEqual(error.data, {"file_name": "test.json"})

    def test_runtime_error(self):
        error = BuilderError.runtime_error("Something went wrong")
        self.assertEqual(error.key, ErrorKey.RUNTIME_ERROR)
        self.assertEqual(error.data, {"error": "Something went wrong"})


if __name__ == "__main__":
    unittest.main()
