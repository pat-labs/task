from typing import List, NamedTuple


class DtoNewTask(NamedTuple):
    task_id: str
    title: str
    task_tags: List[str]
    status: str
    user_assigned_id: str
    user_wrote_id: str
