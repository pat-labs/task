from datetime import datetime

from src.domain.constants.Constants import Constants


class Identifier:
    @staticmethod
    def get_datetime_identifier():
        return datetime.now().strftime(Constants.DATE_TIME_FORMAT)
