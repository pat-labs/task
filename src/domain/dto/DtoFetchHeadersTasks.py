from typing import List, NamedTuple


class DtoFetchHeadersTasks(NamedTuple):
    task_id: str
    title: str
    task_tags: List[str]
    status: str
    user_assigned_id: str
