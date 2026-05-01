from typing import Protocol


class ServiceUser(Protocol):
    driving_component = "SERVICE_USER"

    def user_exists(self, user_id: str) -> bool:
        pass
