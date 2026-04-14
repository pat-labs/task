from typing import List, NamedTuple


class Event(NamedTuple):
    timestamp: str
    event: str
    cls: str
    message: str
