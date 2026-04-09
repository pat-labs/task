import json
from typing import Dict, List, Optional

from src.domain.config.Error import Error
from src.domain.enum.ErrorKey import ErrorKey
from src.domain.enum.ErrorKeyRepository import ErrorKeyRepository


class BuilderErrorMessage:
    _default_messages: Dict[str, str] = {
        ErrorKey.NOT_IN_ENUM.value: "The {attr} is not present in {values}",
        ErrorKey.NOT_UNIQUE_VALUES.value: "The {attr} values must be unique",
        ErrorKey.REQUIRED.value: "New required message {attr}",
        ErrorKey.INVALID_FORMAT.value: "New invalid date_format message {pattern}",
        ErrorKey.INVALID_VALUE.value: "New invalid value message {value}",
        ErrorKey.MAX_SIZE.value: "The current size must be: {max_size}",
        ErrorKey.CAST_FAIL.value: "The {cls} fail to cast the input",
        ErrorKeyRepository.DUPLICATE_KEY.value: "The {identifier} exists",
        ErrorKeyRepository.ENTITY_NOT_EXISTS.value: "The {identifier} is not present in repository",
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

            # Combine all keys from both enums
            valid_keys = list(ErrorKey.__members__.keys()) + list(
                ErrorKeyRepository.__members__.keys()
            )

            for key in data.keys():
                if key not in valid_keys:
                    raise ValueError(f"Invalid error key in JSON: {key}")

            self._messages.update(data)

        except FileNotFoundError:
            raise RuntimeError(f"Error message file not found: {path}")
        except json.JSONDecodeError:
            raise RuntimeError("Invalid JSON date_format in error message file")

    def _format(self, error_key: ErrorKey | ErrorKeyRepository, **kwargs) -> str:
        template = self._messages.get(error_key.value)

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

    def invalid_value(self, attr, value) -> Error:
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

    def not_unique_values(self, attr: str):
        return Error(
            key=ErrorKey.NOT_UNIQUE_VALUES,
            message=self._format(ErrorKey.NOT_UNIQUE_VALUES, attr=attr),
        )

    def not_in_enum(self, attr: str, values: List):
        return Error(
            key=ErrorKey.NOT_IN_ENUM,
            message=self._format(
                ErrorKey.NOT_IN_ENUM, attr=attr, values=", ".join(values)
            ),
        )

    def cast_fail(self, cls: str):
        return Error(
            key=ErrorKey.CAST_FAIL, message=self._format(ErrorKey.CAST_FAIL, cls=cls)
        )

    # -------------------------
    # Builders Driving
    # -------------------------

    def duplicate_key(self, attr: str, value) -> Error:
        return Error(
            key=ErrorKeyRepository.DUPLICATE_KEY,
            message=self._format(
                ErrorKeyRepository.DUPLICATE_KEY,
                attr=attr,
                identifier=value,
            ),
        )

    def entity_not_exists(self, attr: str, value) -> Error:
        return Error(
            key=ErrorKeyRepository.ENTITY_NOT_EXISTS,
            message=self._format(
                ErrorKeyRepository.ENTITY_NOT_EXISTS,
                attr=attr,
                identifier=value,
            ),
        )
