import json
import logging
from datetime import datetime

from src.domain.config.LogEntry import LogEntry


class JsonNamedTupleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        traceback = ""
        if record.exc_info:
            traceback = self.formatException(record.exc_info)

        log_entry = LogEntry(
            timestamp=datetime.fromtimestamp(record.created).isoformat(),
            level=record.levelname,
            logger=record.name,
            message=record.getMessage(),
            module=record.module,
            func_name=record.funcName,
            line_no=record.lineno,
            traceback=traceback.splitlines() if traceback else [],
        )

        return json.dumps(log_entry._asdict(), ensure_ascii=False)
