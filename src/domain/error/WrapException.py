from functools import wraps
import click

from src.domain.error.ExceptionDomain import ExceptionDomain
from src.domain.error.ExceptionDriven import ExceptionDriven


def wrap_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ExceptionDomain as e:
            click.echo(f"Domain Error: {', '.join(e.exceptions)}", err=True)
        except ExceptionDriven as e:
            click.echo(f"Driven Error: {e.key_exception}", err=True)
        except Exception as e:
            click.echo(f"Unexpected Error: {str(e)}", err=True)
        return None

    return wrapper
