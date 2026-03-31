from typing import NamedTuple, List


class DtoNewTask(NamedTuple):
    task_id: str
    tittle: str
    task_tags: List[str]
    status: str
    user_assigned_id: str
    user_wrote_id: str
