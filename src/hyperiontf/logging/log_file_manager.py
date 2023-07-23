"""
Module: Hyperion Test Framework Log File Initialization
=======================================================

This module provides functions for initializing test-specific log files in the Hyperion Test Framework. Test-specific log files are created based on the test name, allowing for separate log files for each test executed while maintaining a singleton instance of the logger.

Requirements:
--------------
- Python 3.6 or higher.
- Required external modules:
  - hyperiontf.configuration for configuration settings.
  - .file_handler.FileHandler from the same package for log file handling.
  - re module for regular expression operations.
  - os module for file path operations.
"""

from hyperiontf.configuration import config
from .file_handler import FileHandler
import re
import os


def generate_test_log_filename(test_name: str) -> str:
    """
    Generate a test-specific log filename based on the provided test name.

    The generated filename includes the test name and an index, if necessary, to ensure uniqueness in case multiple tests
    have the same name.

    :param test_name: The name of the test for which the log file needs to be generated.
    :type test_name: str

    :return: The generated test-specific log filename.
    :rtype: str
    """
    index = 0
    escaped_test_name = re.sub(r"\W", "_", test_name)

    def generate_name():
        return (
            f"{os.getcwd()}/{config.logger.log_folder}/{escaped_test_name}-{index}.html"
        )

    filename = generate_name()
    while os.path.exists(filename):
        index += 1
        filename = generate_name()

    return filename


def init_test_log(test_name: str):
    """
    Initialize a test-specific log file with the given test name.

    This function creates a test-specific log file using the provided test name. The log file is initialized using the
    FileHandler class from the Hyperion Test Framework.

    :param test_name: The name of the test for which the log file needs to be initialized.
    :type test_name: str
    """
    FileHandler().init_file(generate_test_log_filename(test_name))
