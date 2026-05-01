from typing import List

from src.domain.enum.ErrorKey import ErrorKey
from src.domain.error.Error import Error


class BuilderError:
    @staticmethod
    def required(attr: str) -> Error:
        return Error(key=ErrorKey.REQUIRED, data={"attr": attr})

    @staticmethod
    def invalid_format(attr: str, pattern: str) -> Error:
        return Error(
            key=ErrorKey.INVALID_FORMAT, data={"attr": attr, "pattern": pattern}
        )

    @staticmethod
    def invalid_value(attr: str, value: str) -> Error:
        return Error(key=ErrorKey.INVALID_VALUE, data={"attr": attr, "value": value})

    @staticmethod
    def max_size(attr: str, max_size: int) -> Error:
        return Error(key=ErrorKey.MAX_SIZE, data={"attr": attr, "max_size": max_size})

    @staticmethod
    def invalid_size(attr: str, size: int):
        return Error(key=ErrorKey.INVALID_SIZE, data={"attr": attr, "size": size})

    @staticmethod
    def not_unique_values(attr: str) -> Error:
        return Error(key=ErrorKey.NOT_UNIQUE_VALUES, data={"attr": attr})

    @staticmethod
    def not_in_enum(attr: str, value: str, values: List) -> Error:
        return Error(
            key=ErrorKey.NOT_IN_ENUM,
            data={"attr": attr, "value": value, "values": values},
        )

    @staticmethod
    def cast_fail(attr: str, cls: str) -> Error:
        return Error(key=ErrorKey.CAST_FAIL, data={"attr": attr, "cls": cls})

    @staticmethod
    def duplicate_key(attr: str, value) -> Error:
        return Error(key=ErrorKey.DUPLICATE_KEY, data={"attr": attr, "value": value})

    @staticmethod
    def entity_not_exists(attr: str, value) -> Error:
        return Error(
            key=ErrorKey.ENTITY_NOT_EXISTS, data={"attr": attr, "value": value}
        )

    @staticmethod
    def file_not_found(path: str) -> Error:
        return Error(key=ErrorKey.FILE_NOT_FOUND, data={"path": path})

    @staticmethod
    def invalid_json_format(file_name: str) -> Error:
        return Error(key=ErrorKey.INVALID_JSON_FORMAT, data={"file_name": file_name})

    @staticmethod
    def runtime_error(error_msg: str) -> Error:
        return Error(key=ErrorKey.RUNTIME_ERROR, data={"error": error_msg})
