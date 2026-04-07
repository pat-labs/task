import json
from typing import Dict


class BuilderErrorMessage:

    # Default messages
    _default_messages: Dict[str, str] = {
        ErrorKey.REQUIRED.value: "New required message {attr}",
        ErrorKey.INVALID_FORMAT.value: "New invalid format message {pattern}",
        ErrorKey.MAX_SIZE.value: "The current size must be: {max_size}",
    }

    def __init__(self):
        # Active messages (can be overridden)
        self._messages = self._default_messages.copy()

    # -------------------------
    # Load overrides from JSON
    # -------------------------
    def load_from_file(self, path: str) -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("JSON must contain an object")

            # Validate keys against Enum
            for key in data.keys():
                if key not in ErrorKey.__members__:
                    raise ValueError(f"Invalid error key in JSON: {key}")

            # Override defaults
            self._messages.update(data)

        except FileNotFoundError:
            raise RuntimeError(f"Error message file not found: {path}")
        except json.JSONDecodeError:
            raise RuntimeError("Invalid JSON format in error message file")

    # -------------------------
    # Safe formatter
    # -------------------------
    def _format(self, error_key: ErrorKey, **kwargs) -> str:
        template = self._messages.get(error_key.value)

        if not template:
            raise RuntimeError(f"Missing error message for {error_key.value}")

        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise RuntimeError(
                f"Missing format parameter {e.args[0]} for {error_key.value}"
            )

    # -------------------------
    # Builders
    # -------------------------
    def required(self, attr: str) -> ModelError:
        return ModelError(
            key=ErrorKey.REQUIRED,
            message=self._format(ErrorKey.REQUIRED, attr=attr),
        )

    def invalid_format(self, attr: str, pattern: str) -> ModelError:
        return ModelError(
            key=ErrorKey.INVALID_FORMAT,
            message=self._format(
                ErrorKey.INVALID_FORMAT,
                attr=attr,
                pattern=pattern,
            ),
        )

    def invalid_value(self, attr, value) -> ModelError:
        return ModelError(
            key=ErrorKey.INVALID_VALUE,
            message=self._format(
                ErrorKey.INVALID_VALUE,
                attr=attr,
                pattern=value,
            ),
        )

    def max_size(self, attr: str, max_size: int) -> ModelError:
        return ModelError(
            key=ErrorKey.MAX_SIZE,
            message=self._format(
                ErrorKey.MAX_SIZE,
                attr=attr,
                max_size=max_size,
            ),
        )
