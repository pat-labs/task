import logging
import logging.config
import os


class BuilderLogger:
    def __init__(
        self,
        console_log_level: str = "INFO",
        json_log_level: str = "INFO",
        json_log_dir: str = None,
    ):
        self._console_log_level = console_log_level
        self._json_log_level = json_log_level
        self._json_log_dir = os.path.abspath(json_log_dir) if json_log_dir else None
        self._configured = False

    def build(self):
        handlers = {}
        loggers = {}

        # Console Handler
        console_handler_name = "console_handler"
        handlers[console_handler_name] = {
            "class": "logging.StreamHandler",
            "level": self._console_log_level,
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        }

        # JSON File Handler
        json_file_handler_name = "json_file_handler"
        if self._json_log_dir:
            handlers[json_file_handler_name] = {
                "class": "src.driving.config.JsonArrayHandler.JsonDailyArrayHandler",
                "level": self._json_log_level,
                "formatter": "json",
                "log_dir": self._json_log_dir,
                "encoding": "utf-8",
            }

        # Define the 'console_logger'
        loggers["console_logger"] = {
            "level": self._console_log_level,
            "handlers": [console_handler_name],
            "propagate": False,  # Prevent messages from going to root console_log
        }

        # Define the 'json_event_logger'
        if self._json_log_dir:
            loggers["json_event_logger"] = {
                "level": self._json_log_level,
                "handlers": [json_file_handler_name],
                "propagate": False,  # Prevent messages from going to root console_log
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
            "loggers": loggers,  # Use 'loggers' key for named loggers
            "root": {  # Keep root console_log minimal or empty if named loggers are primary
                "level": "WARNING",  # Default root level, can be adjusted
                "handlers": [],  # No handlers for root by default to avoid duplicates
            },
        }

        logging.config.dictConfig(config)
        self._configured = True
        return self

    def get_logger(self, name: str) -> logging.Logger:
        if not self._configured:
            raise RuntimeError("Logger not configured. Call build() first.")
        # User will request 'console_logger' or 'json_event_logger'
        return logging.getLogger(name)
