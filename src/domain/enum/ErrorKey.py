from enum import Enum


class ErrorKey(str, Enum):
    NOT_IN_ENUM = ("NOT_IN_ENUM", "The {attr} is not present in {values}")
    NOT_UNIQUE_VALUES = ("NOT_UNIQUE_VALUES", "The {attr} values must be unique")
    REQUIRED = ("REQUIRED", "Field {attr} is required")
    INVALID_FORMAT = (
        "INVALID_FORMAT",
        "Invalid format for {attr}. Expected pattern: {pattern}",
    )
    INVALID_VALUE = (
        "INVALID_VALUE",
        "Invalid linked_value '{linked_value}' for {attr}",
    )
    MAX_SIZE = ("MAX_SIZE", "The maximum size for {attr} is {max_size}")
    INVALID_SIZE = ("INVALID_SIZE", "The size of {attr} must be {size}")
    CAST_FAIL = ("CAST_FAIL", "Failed to cast input to {cls}")
    DUPLICATE_KEY = (
        "DUPLICATE_KEY",
        "An entity with {attr}='{util}' already exists",
    )
    ENTITY_NOT_EXISTS = (
        "ENTITY_NOT_EXISTS",
        "No entity found with {attr}='{util}'",
    )
    FILE_NOT_FOUND = ("FILE_NOT_FOUND", "File not found: {path}")
    INVALID_JSON_FORMAT = (
        "INVALID_JSON_FORMAT",
        "Invalid JSON format in file: {file_name}",
    )
    RUNTIME_ERROR = ("RUNTIME_ERROR", "Unexpected error: {error}")

    def __new__(cls, value: str, template: str):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.template = template
        return obj

    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)
