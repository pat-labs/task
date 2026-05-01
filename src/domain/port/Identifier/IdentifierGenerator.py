from typing import Protocol


class IdentifierGenerator(Protocol):
    @staticmethod
    def generate() -> str:
        pass
