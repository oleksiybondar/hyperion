"""
Module: Hyperion Test Framework Logger
======================================

This module provides a custom logger implementation tailored for the Hyperion Test Framework. The logger includes custom
features for generating test-specific log files and managing log depth for improved logging and traceability.

Requirements:
--------------
- Python 3.6 or higher.
- Required external modules:
  - json module for working with JSON data.
  - logging module for basic logging functionality.
  - os module for file path operations.
  - re module for regular expression operations.
  - hyperiontf.configuration for configuration settings.
  - .file_handler.FileHandler and .formatter.Formatter from the same package for custom log handling.

Classes:
--------
Logger
"""

import json
import logging
from typing import Optional, cast

from .file_handler import FileHandler as HyperionFileHandler
from .log_depth_manager import LogDepthManager
from .log_file_manager import generate_test_log_filename

END_OF_FOLDER_LEVEL = 10000
END_OF_FOLDER_MESSAGE = "---EOF---"


class Logger(logging.Logger):
    """
    A custom logger for the Hyperion Testing Framework.

    This custom logger extends the functionality of the standard `logging.Logger` class and includes custom features
    specific to the Hyperion Testing Framework. It provides support for generating test-specific log files, managing log
    depth for better traceability, and adding metadata to log records.

    Attributes:
    -----------
    _depth_manager : LogDepthManager
        An instance of the LogDepthManager class that handles the management of the logging depth, allowing for proper
        indentation of log messages.
    """

    def __init__(self, name, level=logging.DEBUG):
        """
        Initialize the logger with a name and an optional level.

        :param name: The name of the logger.
        :type name: str
        :param level: The logging level for the logger. Default is logging.DEBUG.
        :type level: int
        """
        super().__init__(name, level)
        self._depth_manager = LogDepthManager()
        self._file_handler = HyperionFileHandler()
        self.addHandler(self._file_handler)

    def push_folder(self, message: Optional[str] = None):
        """
        Increase the log depth and optionally log a message with the current log depth.

        :param message: Optional message to be logged with the current log depth.
        :type message: str
        """
        self._depth_manager.increase_depth()
        if message:
            self.debug(message)

    def add_meta(self, key: str, value):
        """
        Log metadata with a specified key and value.

        :param key: The key for the metadata.
        :type key: str
        :param value: The value of the metadata.
        :type value: Any
        """
        self.debug(json.dumps(value), extra={"metakey": key})

    def pop_folder(self):
        """
        Decrease the log depth.
        """
        self._depth_manager.decrease_depth()
        self._pop_folder_entry()

    def pop_all(self):
        """
        Reset the log depth to zero.
        """
        self._depth_manager.reset_depth()
        self._pop_folder_entry()

    def merge_logger_stream(self, name: str):
        """
        Merge the logger stream with an existing logger identified by its name.

        :param name: The name of the existing logger to be merged.
        :type name: str
        """
        logger = logging.getLogger(name)
        logger.setLevel(END_OF_FOLDER_LEVEL)
        logger.addHandler(self._file_handler)

    def init_test_log(self, test_name: str):
        """
        Initialize a test-specific log file with the given test name.

        :param test_name: The name of the test for which the log file needs to be initialized.
        :type test_name: str
        """
        self.init_log_file(generate_test_log_filename(test_name))

    def init_log_file(self, new_name: str):
        """
        Initialize the log file with the specified name.

        :param new_name: The name of the log file to be initialized.
        :type new_name: str
        """
        self._file_handler.init_file(new_name)

    def _pop_folder_entry(self):
        self.log(END_OF_FOLDER_LEVEL, END_OF_FOLDER_MESSAGE)


def getLogger(name: str = "TestCase") -> Logger:
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.

    :param name: The name of the logger to be returned. Default is 'TestCase'.
    :type name: str

    :return: The logger instance with the specified name.
    :rtype: Logger
    """
    default_logger_klass = logging.getLoggerClass()
    logging.setLoggerClass(Logger)
    logger = logging.getLogger(name)
    logging.setLoggerClass(default_logger_klass)
    return cast(Logger, logger)
