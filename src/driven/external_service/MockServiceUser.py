class MockServiceUser:
    driving_component = "TEST_SERVICE_USER"

    def user_exists(self, user_id: str) -> bool:
        return True
