from typing import List, NamedTuple


class DtoFetchHeadersTasks(NamedTuple):
    task_id: str
    tittle: str
    task_tags: List[str]
    status: str
    user_assigned_id: str
