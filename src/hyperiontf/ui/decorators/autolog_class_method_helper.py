"""
Module: Method Auto-Logging Decorator
======================================

This module provides a method decorator and a function to automatically decorate class methods with logging capabilities
 When applied to class methods, the decorator automatically logs method calls, arguments, and return values for easier
 debugging and tracing of program execution.

Requirements:
--------------
- Python 3.6 or higher.
- Required external modules:
  - re (Regular Expression) module for pattern matching.
  - hyperiontf.logging for logging support.
  - hyperiontf.configuration for configuration settings.
  - hyperiontf.helpers.string_helpers for string manipulation.

Functions:
-----------
auto_decorate_class_methods_with_logging

Classes:
---------
AutoLoggingMethod

Module Constants:
------------------

PRIVATE_METHODS_PATTERN:
    A regular expression pattern used to match method names that start with a single '_'.
    By default, private methods will be logged. Set `config.log_private = False` to exclude them from logging.

"""

import re
from hyperiontf.logging import getLogger, Logger
from hyperiontf.configuration import config
from hyperiontf.helpers.string_helpers import method_name_to_human_readable
from typing import Callable, Type, Any
from hyperiontf.helpers.own_methods_helper import get_instance_unique_methods

PRIVATE_METHODS_PATTERN = "^_"


class AutoLoggingMethod:
    def __init__(self, original_method: Callable, sender_name: str, logger: Logger):
        """
        A class that wraps the original method and logs method calls and arguments.

        :param original_method: The original method that will be wrapped and logged.
        :type original_method: Callable

        :param sender_name: The name of the sender (usually the instance name) to include in the log messages.
        :type sender_name: str

        :param logger: The logger object used for logging method calls and arguments.
        :type logger: Logger

        """
        self._name = sender_name
        self._original_method = original_method
        self._logger = logger or getLogger()

    def wrapper(self, *args, **kwargs):
        """
        The method wrapper that logs method calls and arguments.

        :param args: Positional arguments passed to the wrapped method.
        :type args: Tuple

        :param kwargs: Keyword arguments passed to the wrapped method.
        :type kwargs: Dict

        :return: The return value of the wrapped method.
        :rtype: Any

        """
        method_name = self._original_method.__name__
        self._logger.push_folder(
            f"[{self._name}] {method_name_to_human_readable(method_name)}"
        )
        dbg_msg = f"[{self._name}] {method_name}() called with args:\n{args}\n{kwargs}"
        self._logger.debug(dbg_msg)
        result = self._original_method(*args, **kwargs)
        self._logger.pop_folder()
        return result


def auto_decorate_class_methods_with_logging(
    instance: object,
    base_class: Type[object],
    logger: Logger = getLogger(),
):
    """
    Automatically decorates class methods with logging capabilities.

    :param instance: The instance of the class whose methods will be decorated.
    :type instance: object

    :param base_class: The base class to stop the method decoration at. Methods in this class and its ancestors will be
     ignored.
    :type base_class: ClassVar

    :param logger: An optional Logger object for logging method calls and arguments. If not provided, a default logger
     will be used.
    :type logger: Logger, optional

    Usage:
    ------
    1. Create a logger object:
       ```
       from hyperiontf.logging import getLogger, Logger
       logger = getLogger()
       ```

    2. Define your class and its methods. Optionally, set `__full_name__` attribute for the class instance to include a
     sender name in the logs.

    3. Decorate the class methods with automatic logging:
       ```
       from hyperiontf.helpers.string_helpers import method_name_to_human_readable

       class YourClass:
           def __init__(self):
               self.__full_name__ = "YourClassInstance"  # Optional: Include a sender name in the logs
               decorate_class_methods_with_autolog(self, YourClass, logger)

           def your_method(self, arg1, arg2, ...):
               ...


       ```

    Notes:
    ------
    - The decorator does not apply to methods with names starting and ending with '__' (dunder methods).
    - By default, the decorator logs private methods as well. Set `config.log_private = False` to exclude them from
    logging.

    """
    sender_name = ""

    if hasattr(instance, "__full_name__"):
        sender_name = instance.__full_name__

    for method in get_instance_unique_methods(instance, base_class):
        _wrap_method(instance, method, sender_name, logger)


def _is_property(instance: Any, method: str) -> bool:
    """
    Determine if a given method name corresponds to a property of the provided instance.

    Args:
        instance (Any): The object instance to check.
        method (str): The name of the method or attribute to check.

    Returns:
        bool: True if the specified method name is a property, False otherwise.
    """
    # Retrieve the attribute from the class (not the instance) to avoid triggering a property call
    attr = getattr(instance.__class__, method, None)

    # Check if the attribute is a property
    return isinstance(attr, property)


def _wrap_method(instance: Any, method: str, sender_name: str, logger: Any):
    if (
        bool(re.match(PRIVATE_METHODS_PATTERN, method))
        and not config.page_object.log_private
    ):
        return

    if _is_property(instance, method):
        return

    undecorated_method = getattr(instance, method)

    if not callable(undecorated_method):
        return

    setattr(
        instance,
        method,
        AutoLoggingMethod(undecorated_method, sender_name, logger).wrapper,
    )
