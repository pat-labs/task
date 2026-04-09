from typing import NamedTuple, Optional


class LogEntry(NamedTuple):
    timestamp: str
    level: str
    logger: str
    message: str
    module: str
    func_name: str
    line_no: int
    traceback: Optional[str] = None
