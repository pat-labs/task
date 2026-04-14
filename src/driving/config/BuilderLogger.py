import logging
import logging.config
import os


class BuilderLogger:
    def __init__(self, level, log_dir, to_console):
        self._level = level
        self._log_dir = os.path.abspath(log_dir) if log_dir else None
        self._to_console = to_console
        self._configured = False

    def build(self):
        handlers = {}

        if self._to_console:
            handlers["console"] = {
                "class": "logging.StreamHandler",
                "level": self._level,
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            }

        if self._log_dir:
            handlers["file"] = {
                "class": "src.driving.config.JsonArrayHandler.JsonDailyArrayHandler",
                "level": self._level,
                "formatter": "json",
                "log_dir": self._log_dir,
                "encoding": "utf-8",
            }

        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "json": {
                    "()": "src.driving.config.JsonFormatter.JsonNamedTupleFormatter",
                },
            },
            "handlers": handlers,
            "root": {
                "level": self._level,
                "handlers": list(handlers.keys()),
            },
        }

        logging.config.dictConfig(config)
        self._configured = True
        return self

    def get_logger(self, name: str = None) -> logging.Logger:
        if not self._configured:
            raise RuntimeError("Logger not configured. Call build() first.")
        return logging.getLogger(name)
