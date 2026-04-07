from enum import Enum, auto


class ErrorKeyRepository(Enum):
    REPOSITORY_DUPLICATE_KEY = auto()
    REPOSITORY_ENTITY_NOT_EXISTS = auto()
