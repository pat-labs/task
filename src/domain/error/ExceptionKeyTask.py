from enum import Enum, auto


class ExceptionKeyTask(Enum):
    TASK_TASK_TAGS_IS_NOT_SET = auto()
    TASK_TASK_IDS_IS_NOT_SET = auto()
    TASK_STATUS_INVALID_FORMAT = auto()
    TASK_TITTLE_INVALID_FORMAT = auto()
    TASK_DESCRIPTION_INVALID_FORMAT = auto()
    TASK_ID_INVALID_FORMAT = auto()
