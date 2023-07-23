"""
Module: Exception Handling Decorator
=============================

This module contains a Python decorator that can be used to catch exceptions that may occur during the execution of a
function and log them in a graceful manner, preventing any failures from propagating beyond the decorated function.

The decorator is designed to wrap any function with exception handling capabilities, allowing the function's code to
execute without crashing even if exceptions are raised. Instead, the exceptions are logged using a provided logger or a
default logger.

Usage:
------
1. Import the decorator function:
2. Decorate the desired functions using the `without_failure` decorator:
3. When `your_function` is called, any exceptions that occur within the function will be caught and logged without
interrupting the overall program flow.

"""

import logging
from hyperiontf.logging import getLogger, Logger
from typing import Callable, Optional


def without_failure(
    logger: Optional[Logger | logging.Logger] = None,
) -> Callable | property:
    """
    A decorator that catches any exception occurring during function execution and logs it, ensuring the failure is
    handled gracefully.

    :param logger: An optional Logger object to log the exceptions. If not provided, a default logger named
                   'withoutFailuresLogger' will be used.
    :return: The decorated function.
    """
    if logger is None:
        logger = getLogger("withoutFailuresLogger")

    def inner_decorator(method: Callable) -> Callable | property:
        """
        Inner decorator function to wrap the provided method with exception handling.

        :param method: The function to be decorated.
        :return: The decorated function with exception handling.
        """

        def decorator(*args, **kwargs) -> object:
            """
            The actual decorated code that invokes the wrapped function with exception handling.

            :param args: Positional arguments to be passed to the wrapped function.
            :param kwargs: Keyword arguments to be passed to the wrapped function.
            :return: The result of the wrapped function if successful, None if an exception occurs.
            """
            try:
                return method(*args, **kwargs)
            except Exception as e:
                logger.debug(f"{e.__class__.__name__}: {e}")
                return None

        return decorator

    return inner_decorator
