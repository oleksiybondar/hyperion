"""
Module: Hyperion Testing Framework Log Depth Manager
=================================================

This module provides a singleton class, LogDepthManager, for managing the logging depth. The logging depth is a
class-level attribute that tracks the level of nested logging, allowing for indentation of log messages to indicate
hierarchical relationships.

"""

from hyperiontf.helpers.decorators.singleton import Singleton


@Singleton
class LogDepthManager:
    """
    A singleton class for managing the logging depth.

    The LogDepthManager class is a singleton that provides methods to increase, decrease, and reset the logging depth.
    The logging depth is used to indicate the level of nested logging, and it is a class-level attribute to ensure
    consistent behavior across different instances.

    Attributes:
    -----------
    log_depth : int
        A class-level attribute to track the logging depth. The depth value can be used to indicate the level of nested
        logging.
    """

    def __init__(self):
        """
        Initialize the LogDepthManager with an initial logging depth of zero.
        """
        self.log_depth = 0

    def increase_depth(self):
        """
        Increment the logging depth by one.
        """
        self.log_depth += 1

    def decrease_depth(self):
        """
        Decrement the logging depth by one, if it is greater than zero.
        """
        if self.log_depth > 0:
            self.log_depth -= 1

    def reset_depth(self):
        """
        Reset the logging depth to zero.
        """
        self.log_depth = 0
