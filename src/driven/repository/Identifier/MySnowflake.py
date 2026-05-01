import asyncio

from snowflakekit import SnowflakeConfig, SnowflakeGenerator


class MySnowflake:
    _config = SnowflakeConfig(
        epoch=1609459200000,
        node_id=1,
        worker_id=2,
        time_bits=39,
        node_bits=5,
        worker_bits=8,
    )

    _generator = SnowflakeGenerator(config=_config)

    @staticmethod
    def generate() -> str:
        new_loop_created = False
        try:
            loop = asyncio.get_running_loop()
            import nest_asyncio

            nest_asyncio.apply()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            new_loop_created = True

        try:
            identifier = loop.run_until_complete(MySnowflake._generator.generate())
            return str(identifier)
        finally:
            if new_loop_created:
                loop.close()
