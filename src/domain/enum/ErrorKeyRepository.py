from enum import Enum


class ErrorKeyRepository(str, Enum):
    DUPLICATE_KEY = "DUPLICATE_KEY"
    ENTITY_NOT_EXISTS = "ENTITY_NOT_EXISTS"
