from typing import Protocol

from src.domain.enum.DrivingComponent import DrivingComponent


class ServiceUser(Protocol):
    driving_component: DrivingComponent

    def user_exists(self, user_id: str) -> bool:
        pass
