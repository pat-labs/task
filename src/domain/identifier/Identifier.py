from datetime import datetime


class Identifier:
    @staticmethod
    def get_datetime_identifier(format: str):
        return datetime.now().strftime(format)
