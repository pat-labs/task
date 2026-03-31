from src.domain.constants.Constants import Constants


class AuditUtil:
    @staticmethod
    def get_sql_query():
        return f"""
                audit_id VARCHAR({Constants.USER_ID_MAX_SIZE}),
                user_wrote_id VARCHAR({Constants.USER_ID_MAX_SIZE}),
                updated_at VARCHAR({Constants.DATE_TIME_FORMAT_MAX_SIZE}),
                user_created_id VARCHAR({Constants.USER_ID_MAX_SIZE}),
                created_at VARCHAR({Constants.DATE_TIME_FORMAT_MAX_SIZE})
                """
