from typing import Protocol


class ServiceUser(Protocol):
    def is_not_valid_user(self, user_id: str) -> bool:
        pass
