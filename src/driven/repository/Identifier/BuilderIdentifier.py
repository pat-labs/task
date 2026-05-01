from src.driven.repository.Identifier.MySnowflake import MySnowflake


class BuildIdentifier:
    @staticmethod
    def generate():
        return MySnowflake.generate()
