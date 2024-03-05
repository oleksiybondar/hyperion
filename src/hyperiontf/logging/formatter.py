"""
Module: Custom HTML Logging Formatter
======================================

This module defines a custom `Formatter` class for logging in HTML format. The `Formatter` is based on the standard
`logging.Formatter` but extends its functionality to log messages with additional metadata, such as log level,
timestamp, file path, line number, and optional custom data.

Classes:
---------
Formatter
"""

import logging
import html
import json
import datetime
from .log_depth_manager import LogDepthManager


class Formatter(logging.Formatter):
    """
    A custom `Formatter` for logging messages in HTML format with additional metadata.

    This `Formatter` extends the functionality of the standard `logging.Formatter` class to include custom metadata in
    the logged messages. It adds support for logging in HTML format and escaping special characters in the logged data.
    """

    def __init__(
        self, fmt=None, datefmt=None, style="%", validate=True, *, defaults=None
    ):
        """
        Initialize the formatter with specified format strings.

        Initialize the formatter either with the specified format string, or a
        default as described above. Allow for specialized date formatting with
        the optional datefmt argument. If datefmt is omitted, you get an
        ISO8601-like (or RFC 3339-like) format.

        Use a style parameter of '%', '{' or '$' to specify that you want to
        use one of %-formatting, :meth:`str.format` (``{}``) formatting or
        :class:`string.Template` formatting in your format string.

        .. versionchanged:: 3.2
           Added the ``style`` parameter.
        """
        super().__init__(
            fmt=fmt, datefmt=datefmt, style=style, validate=validate, defaults=defaults
        )
        self._depth_manager = LogDepthManager()

    def _get_basic_log_data(self, record: logging.LogRecord) -> dict:
        """
        Extract the minimum required data from the log record and return it as a dictionary.
        """
        return {
            "lvl": record.levelno,
            "msg": record.getMessage(),
            "name": record.name,
            "time": self._format_time_with_milliseconds(record.created),
            "depth": self._depth_manager.log_depth,
            "fPath": record.pathname,
            "fLine": record.lineno,
        }

    def _format_time_with_milliseconds(self, time) -> str:
        """
        Convert the timestamp to a formatted time string with milliseconds.
        """
        datetime_obj = datetime.datetime.fromtimestamp(time)
        formatted_time = datetime_obj.strftime(self.datefmt or self.default_time_format)
        milliseconds = int(datetime_obj.microsecond / 1000)
        return f"{formatted_time}.{milliseconds}"

    @staticmethod
    def _add_meta_key_to_data(data: dict, record: logging.LogRecord):
        """
        Add a 'key' attribute to the data dictionary if the log record has a 'metakey' attribute.
        """
        if hasattr(record, "metakey"):
            data["key"] = record.metakey

    def _add_exception_info_to_data(self, data: dict, record: logging.LogRecord):
        """
        Add an 'exception' attribute with the formatted exception information if the log record has an 'exc_info'
        attribute.
        """
        if record.exc_info:
            data["exception"] = self.formatException(record.exc_info)

    @staticmethod
    def _add_assertion_to_data(data: dict, record: logging.LogRecord):
        """
        Add an 'assertion' attribute to the data dictionary if the log record has an 'assertion' attribute.
        """
        if hasattr(record, "assertion"):
            data["assertion"] = str(record.assertion).lower()

    @staticmethod
    def _add_attachments_to_data(data: dict, record: logging.LogRecord):
        """
        Add an 'attachments' attribute to the data dictionary if the log record has an 'attachments' attribute.
        """
        if hasattr(record, "attachments"):
            data["attachments"] = json.dumps(record.attachments)

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record into an HTML-escaped JSON string with additional metadata.
        """
        data = self._get_basic_log_data(record)
        self._add_meta_key_to_data(data, record)
        self._add_exception_info_to_data(data, record)
        self._add_assertion_to_data(data, record)
        self._add_attachments_to_data(data, record)
        return html.escape(json.dumps(data))
