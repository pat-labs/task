import json
import logging
import os
from datetime import datetime

from src.domain.constants.Constants import Constants


class JsonDailyArrayHandler(logging.Handler):
    """Handler that manages logs in daily files named YYYYMMDD.json as JSON arrays."""

    def __init__(self, log_dir: str, encoding: str = "utf-8"):
        super().__init__()
        self.log_dir = os.path.abspath(log_dir) if log_dir else "."
        self.encoding = encoding
        os.makedirs(self.log_dir, exist_ok=True)

    def _get_current_filepath(self) -> str:
        date_str = datetime.now().strftime(Constants.DATE_FORMAT)
        return os.path.join(self.log_dir, f"{date_str}.json")

    def emit(self, record):
        try:
            file_path = self._get_current_filepath()

            # Initialize file as an empty array if it doesn't exist or is empty
            if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
                with open(file_path, "w", encoding=self.encoding) as f:
                    f.write("[]")

            # Get the formatted JSON string from the formatter
            msg = self.format(record)
            entry = json.loads(msg)

            # Read current data, append, and overwrite
            with open(file_path, "r", encoding=self.encoding) as f:
                data = json.load(f)

            data.append(entry)

            with open(file_path, "w", encoding=self.encoding) as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception:
            self.handleError(record)
