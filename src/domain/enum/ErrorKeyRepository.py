from enum import Enum, auto


class ErrorKeyRepository(str, Enum):
    DUPLICATE_KEY = "DUPLICATE_KEY"
    ENTITY_NOT_EXISTS = "ENTITY_NOT_EXISTS"
