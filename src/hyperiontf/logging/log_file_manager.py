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
from pathlib import Path


def generate_test_log_filename(test_name: str) -> str:
    """
    Generate a unique, test-specific HTML log file path.

    This function:
    - derives a filesystem-safe name from the provided test name
    - uses `config.logger.log_folder` as the base directory
    - supports both absolute and relative log folder paths
    - ensures the log directory exists
    - guarantees uniqueness by appending a numeric index suffix

    The returned path always points to a non-existing file at the time of generation.

    Parameters:
        test_name (str): Name of the test for which the log file is generated.

    Returns:
        str: Absolute path to a unique HTML log file.
    """
    escaped_test_name = re.sub(r"\W", "_", test_name)

    log_dir = Path(config.logger.log_folder)

    # Defensive: if log_folder ever becomes relative, resolve it under PWD.
    if not log_dir.is_absolute():
        log_dir = Path(os.getcwd()) / log_dir

    # Defensive: ensure the folder exists even if logger init did not run as expected.
    log_dir.mkdir(parents=True, exist_ok=True)

    return str(enumerate_valid_log_path(log_dir, escaped_test_name))


def enumerate_valid_log_path(log_dir: Path, name: str):
    """
    Enumerate a non-existing log file path within a directory.

    The function checks for existing files and increments a numeric suffix
    until a free filename is found.

    Example:
        name-0.html
        name-1.html
        name-2.html
        ...

    Parameters:
        log_dir (Path): Directory where log files are stored.
        name (str): Base filename (without index or extension).

    Returns:
        str: Path to a non-existing log file.
    """
    index = 0
    path = generate_path(log_dir, name, index)
    while path.exists():
        index += 1
        path = generate_path(log_dir, name, index)

    return str(path)


def generate_path(log_dir: Path, name: str, i: int) -> Path:
    """
    Construct a log file path using a base name and numeric index.

    Parameters:
        log_dir (Path): Directory where the log file will be created.
        name (str): Base filename (already sanitized).
        i (int): Index used to ensure filename uniqueness.

    Returns:
        Path: Full path to the indexed HTML log file.
    """
    return log_dir / f"{name}-{i}.html"


def init_test_log(test_name: str):
    """
    Initialize a test-specific log file with the given test name.

    This function creates a test-specific log file using the provided test name. The log file is initialized using the
    FileHandler class from the Hyperion Test Framework.

    :param test_name: The name of the test for which the log file needs to be initialized.
    :type test_name: str
    """
    FileHandler().init_file(generate_test_log_filename(test_name))
