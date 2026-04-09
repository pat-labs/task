from src.domain.enum.DrivingComponent import DrivingComponent


class WebClientUser:
    driving_component = DrivingComponent.SERVICE

    def __init__(self):
        pass

    def user_exists(self, user_id: str) -> bool:
        if user_id:
            return True
        return False
