from datetime import datetime

from src.domain.constants.Constants import Constants


class Identifier:
    @staticmethod
    def get_datetime_identifier(format: str):
        return datetime.now().strftime(format)
