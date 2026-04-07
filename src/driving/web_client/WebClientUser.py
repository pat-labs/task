class WebClientUser:
    def __init__(self):
        pass

    def is_not_valid_user(self, user_id: str) -> bool:
        if user_id:
            return True
        return False
