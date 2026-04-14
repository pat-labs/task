import re
from datetime import datetime
from enum import Enum
from typing import List, Type

from src.domain.constants.Constants import Constants


class Util:
    @staticmethod
    def has_duplicates(data: List) -> bool:
        return len(data) != len(set(data))

    @staticmethod
    def has_name(enum_class: Type[Enum], name: str) -> bool:
        return name in enum_class.__members__

    @staticmethod
    def is_match(text: str, pattern: str) -> bool:
        if text is None or pattern is None:
            return False
        return bool(re.match(pattern, text))

    @staticmethod
    def is_not_valid_format_user(user_id: str) -> bool:
        return len(user_id) > Constants.USER_ID_MAX_SIZE

    @staticmethod
    def is_not_valid_datetime_format(date: str):
        try:
            return date != datetime.strptime(date, Constants.DATE_TIME_FORMAT).strftime(
                Constants.DATE_TIME_FORMAT
            )
        except (ValueError, TypeError):
            return True
