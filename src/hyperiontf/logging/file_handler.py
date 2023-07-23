"""
Module: Custom FileHandler for HTML Logging
===========================================

This module defines a custom `FileHandler` class for logging in HTML format. The `FileHandler` is based on the standard
`logging.FileHandler` but has some additional functionality and is implemented as a Singleton.

Requirements:
--------------
- Python 3.6 or higher.
- Required external modules:
  - logging module for basic logging functionality.
  - io.TextIOWrapper for working with file streams.
  - shutil module for file manipulation.
  - os module for file path operations.

Classes:
---------
FileHandler
"""

import logging
from io import TextIOWrapper
import shutil
import os
from typing import Optional

from hyperiontf.helpers.decorators import Singleton
from .formatter import Formatter


@Singleton
class FileHandler(logging.FileHandler):
    """
    A custom `FileHandler` for logging in HTML format, implemented as a Singleton.

    This `FileHandler` extends the functionality of the standard `logging.FileHandler` and adds support for logging in
    HTML format. Additionally, it implements the Singleton design pattern to ensure only one instance is used for
    logging throughout the application.
    """

    def __init__(
        self,
        filename: str | os.PathLike[str] = "log.html",
        encoding: Optional[str] = "utf-8",
        errors=None,
    ):
        """
        Open the specified file and use it as the stream for logging.
        """
        super().__init__(filename, "a", encoding, True, errors)
        self.setFormatter(Formatter())

    def _open(self) -> TextIOWrapper:
        """
        Open the specified file and return the file stream as a TextIOWrapper.
        :return:
        """
        self._clone_template()
        return logging.FileHandler._open(self)

    def _clone_template(self):
        """
        Copy the HTML template file to the log file destination, ensuring a consistent layout for HTML logging.
        """
        shutil.copy(
            f"{os.path.dirname(os.path.realpath(__file__))}/assets/template.html",
            self.baseFilename,
        )

    def init_file(self, new_file: str):
        """
        Reinitialize the `FileHandler` with a new log file.

        :param new_file:
        :return:
        """
        self.close()  # Close the current file if it's open
        self.baseFilename = os.fspath(new_file)  # Update the file name
        self._open()  # Reopen the file with the new name
