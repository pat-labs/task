from datetime import datetime


class Identifier:
    @staticmethod
    def get_datetime_identifier(date_format: str):
        return datetime.now().strftime(date_format)
