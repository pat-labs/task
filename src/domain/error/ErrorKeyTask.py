from enum import Enum, auto


class ErrorKeyTask(Enum):
    TASK_TAGS_INVALID_VALUE = auto()
    TASK_LINKED_ITEMS_INVALID_VALUE = auto()
    TASK_STATUS_INVALID_VALUE = auto()
    TASK_TASK_TAGS_IS_NOT_SET = auto()
    TASK_linked_items_IS_NOT_SET = auto()
    TASK_STATUS_INVALID_FORMAT = auto()
    TASK_TITLE_INVALID_FORMAT = auto()
    TASK_DESCRIPTION_INVALID_FORMAT = auto()
    TASK_ID_INVALID_FORMAT = auto()
