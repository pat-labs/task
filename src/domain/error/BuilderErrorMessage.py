import json
from typing import Dict, List, Optional

from src.domain.config.Error import Error
from src.domain.enum.ErrorKey import ErrorKey


class BuilderErrorMessage:
    _default_messages: Dict[ErrorKey, str] = {
        ErrorKey.NOT_IN_ENUM: "The {attr} is not present in {values}",
        ErrorKey.NOT_UNIQUE_VALUES: "The {attr} values must be unique",
        ErrorKey.REQUIRED: "New required message {attr}",
        ErrorKey.INVALID_FORMAT: "New invalid date_format message {pattern}",
        ErrorKey.INVALID_VALUE: "New invalid value message {value}",
        ErrorKey.MAX_SIZE: "The current size must be: {max_size}",
        ErrorKey.CAST_FAIL: "The {cls} fail to cast the input",
        ErrorKey.DUPLICATE_KEY: "The {attr} with value {identifier} exists",
        ErrorKey.ENTITY_NOT_EXISTS: "The {attr} with value {identifier} is not present in repository",
        ErrorKey.FILE_NOT_FOUND: "Error message file not found: {path}",
        ErrorKey.INVALID_JSON_FORMAT: "Invalid JSON date_format in error message file",
        ErrorKey.RUNTIME_ERROR: "Unexpected error: {error}",
    }

    def __init__(self, path: Optional[str] = None):
        self._messages = self._default_messages.copy()

        if path:
            self._load_from_file(path)

    def _load_from_file(self, path: str) -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("JSON must contain an object")

            enum_keys_map = {member.value: member for member in ErrorKey}

            for key_str, message in data.items():
                if key_str not in enum_keys_map:
                    raise ValueError(f"Invalid error key in JSON: {key_str}")
                self._messages[enum_keys_map[key_str]] = message

        except FileNotFoundError:
            raise RuntimeError(f"Error message file not found: {path}")
        except json.JSONDecodeError:
            raise RuntimeError("Invalid JSON date_format in error message file")

    def _format(self, error_key: ErrorKey, **kwargs) -> str:
        template = self._messages.get(error_key)

        if not template:
            raise RuntimeError(f"Missing error message for {error_key.value}")

        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise RuntimeError(
                f"Missing date_format parameter {e.args[0]} for {error_key.value}"
            )

    # -------------------------
    # Builders Domain
    # -------------------------
    def required(self, attr: str) -> Error:
        return Error(
            key=ErrorKey.REQUIRED,
            message=self._format(ErrorKey.REQUIRED, attr=attr),
        )

    def invalid_format(self, attr: str, pattern: str) -> Error:
        return Error(
            key=ErrorKey.INVALID_FORMAT,
            message=self._format(
                ErrorKey.INVALID_FORMAT,
                attr=attr,
                pattern=pattern,
            ),
        )

    def invalid_value(self, attr: str, value) -> Error:
        return Error(
            key=ErrorKey.INVALID_VALUE,
            message=self._format(
                ErrorKey.INVALID_VALUE,
                attr=attr,
                value=value,
            ),
        )

    def max_size(self, attr: str, max_size: int) -> Error:
        return Error(
            key=ErrorKey.MAX_SIZE,
            message=self._format(
                ErrorKey.MAX_SIZE,
                attr=attr,
                max_size=max_size,
            ),
        )

    def not_unique_values(self, attr: str) -> Error:
        return Error(
            key=ErrorKey.NOT_UNIQUE_VALUES,
            message=self._format(ErrorKey.NOT_UNIQUE_VALUES, attr=attr),
        )

    def not_in_enum(self, attr: str, values: List) -> Error:
        return Error(
            key=ErrorKey.NOT_IN_ENUM,
            message=self._format(
                ErrorKey.NOT_IN_ENUM, attr=attr, values=", ".join(values)
            ),
        )

    def cast_fail(self, cls: str) -> Error:
        return Error(
            key=ErrorKey.CAST_FAIL, message=self._format(ErrorKey.CAST_FAIL, cls=cls)
        )

    # -------------------------
    # Builders Driving
    # -------------------------

    def duplicate_key(self, attr: str, value) -> Error:
        return Error(
            key=ErrorKey.DUPLICATE_KEY,
            message=self._format(
                ErrorKey.DUPLICATE_KEY,
                attr=attr,
                identifier=value,
            ),
        )

    def entity_not_exists(self, attr: str, value) -> Error:
        return Error(
            key=ErrorKey.ENTITY_NOT_EXISTS,
            message=self._format(
                ErrorKey.ENTITY_NOT_EXISTS,
                attr=attr,
                identifier=value,
            ),
        )

    # -------------------------
    # Builders for general errors (file operations, runtime)
    # -------------------------
    def file_not_found(self, path: str) -> Error:
        return Error(
            key=ErrorKey.FILE_NOT_FOUND,
            message=self._format(ErrorKey.FILE_NOT_FOUND, path=path),
        )

    def invalid_json_format(self) -> Error:
        return Error(
            key=ErrorKey.INVALID_JSON_FORMAT,
            message=self._format(ErrorKey.INVALID_JSON_FORMAT),
        )

    def runtime_error(self, error_msg: str) -> Error:
        return Error(
            key=ErrorKey.RUNTIME_ERROR,
            message=self._format(ErrorKey.RUNTIME_ERROR, error=error_msg),
        )
