from __future__ import annotations

import json
from typing import Dict, Optional

from src.domain.error.BuilderError import BuilderError
from src.domain.error.Error import Error
from src.domain.error.ExceptionDomain import ExceptionDomain


class BuilderErrorMessage:
    message = "Builder Error Message:"

    def __init__(self, path: Optional[str] = None):
        self._overrides: Dict[str, str] = {}

        if path:
            self._load_from_file(path)

    def _load_from_file(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ExceptionDomain(
                    self.message,
                    [BuilderError.invalid_json_format(file_name=path.split("/")[-1])],
                )
            self._overrides = data
        except Exception:
            raise ExceptionDomain(
                self.message,
                [BuilderError.file_not_found(path=path)],
            )

    def format(self, error: Error) -> str:
        template = self._overrides.get(error.key.value, error.key.template)
        return template.format(**error.data)
