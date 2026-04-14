from typing import List, NamedTuple


class LogEntry(NamedTuple):
    timestamp: str
    level: str
    logger: str
    message: str
    module: str
    func_name: str
    line_no: int
    traceback: List[str]
