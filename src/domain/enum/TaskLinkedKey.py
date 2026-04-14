from enum import Enum


class TaskLinkedKey(str, Enum):
    TASK_PARENT = "TASK_PARENT"
    TASK_RELATED = "TASK_RELATED"
