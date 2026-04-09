import json
import logging
from datetime import datetime

from src.domain.model.LogEntry import LogEntry


class JsonNamedTupleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # Extract traceback if present (matches your exc_info=True in WrapException)
        traceback = None
        if record.exc_info:
            traceback = self.formatException(record.exc_info)

        # Create the structured LogEntry
        log_entry = LogEntry(
            timestamp=datetime.fromtimestamp(record.created).isoformat(),
            level=record.levelname,
            logger=record.name,
            message=record.getMessage(),
            module=record.module,
            func_name=record.funcName,
            line_no=record.lineno,
            traceback=traceback,
        )

        # Convert NamedTuple to dict and then to JSON string
        return json.dumps(log_entry._asdict(), ensure_ascii=False)
