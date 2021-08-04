import logging
import sys
from types import TracebackType
from typing import Type

import click
from onix_splitter.splitter import split


def excepthook(
    exception_type: Type[BaseException],
    exception_instance: BaseException,
    exception_traceback: TracebackType,
) -> None:
    """Function called for uncaught exceptions
    :param exception_type: Type of an exception
    :param exception_instance: Exception instance
    :param exception_traceback: Exception traceback
    """
    logging.fatal(
        f"The application crashed. The exception hook has been fired: {exception_instance}",
        exc_info=(exception_type, exception_instance, exception_traceback),
    )


sys.excepthook = excepthook


@click.group()
@click.pass_context
def cli(*args, **kwargs) -> None:  # type: ignore
    """onix-splitter is a tool used for splitting large ONIX collections into 1-item chunks.

    It extracts items with specified identifiers and save them as 1-item ONIX collections
    in the specified output directory.
    """
    pass


cli.add_command(split)
