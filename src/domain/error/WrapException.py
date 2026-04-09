from functools import wraps
from typing import Any, Callable

import click

from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.error.ExceptionDriven import ExceptionDriven


def wrap_exception(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> Any:
        # Attempt to retrieve the logger from the bootstrap attribute of the class instance
        # This assumes the decorated method is an instance method and 'self' has a 'bootstrap' attribute
        logger = getattr(getattr(self, "bootstrap", None), "logger", None)

        try:
            return func(self, *args, **kwargs)
        except ExceptionDomain as e:
            if logger:
                logger.error(
                    f"Domain Error in {func.__name__}: {str(e)}", exc_info=True
                )
            click.echo(f"Domain Error: {str(e)}", err=True)
        except ExceptionDriven as e:
            if logger:
                logger.error(
                    f"Driven Error in {func.__name__}: {str(e)}", exc_info=True
                )
            click.echo(f"Driven Error: {str(e)}", err=True)
        except Exception as e:
            if logger:
                logger.error(
                    f"Unexpected Error in {func.__name__}: {str(e)}", exc_info=True
                )
            click.echo(f"Unexpected Error: {str(e)}", err=True)
        return None

    return wrapper
