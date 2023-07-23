from datetime import timedelta
from typing import Optional, Any, List, Dict, Iterable, Sequence, Union
import collections
import datetime
import time
import difflib
import re
import os

from hyperiontf.logging import getLogger, Logger
from .logging_helper import expect_logging_helper


class Expect:
    """
    The Expect class is a custom-built expectation handler for Python.

    Despite the availability of a number of excellent testing libraries in Python such as pytest, unittest and robot,
    there is no standard, built-in 'expect' functionality. To bridge this gap and to cater to specific needs, this
    custom Expect class was developed.

    Key Reasons for Creating the Custom Expect Class:

    1. Lack of Standard Python Expect: Python does not come with a built-in 'expect' functionality.
       While some testing libraries like pytest and robot do provide this, it doesn't cover all use-cases
       and not always is the preferred choice due to other constraints.

    2. Custom Logging: In complex systems and test environments, logging plays a crucial role. Standard expectation
       handling from existing libraries might not provide the level of customisation and control required over
       logging. The Expect class addresses this by providing an extensible and customizable logging system,
       allowing users to tailor it according to their needs.

    The Expect class provides a robust and flexible framework for managing and asserting expectations,
    integrating seamlessly with existing code and providing detailed logging and error handling capabilities.
    """

    allowed_extensions_for_file_difference = [".txt", ".json", ".xml", ".csv", ".log"]

    @staticmethod
    def add_file_comparison_format(extension: str):
        """
        Add a new file format for comparison in file difference method.

        Args:
            extension (str): The file extension to be added.

        """
        if extension.startswith("."):
            Expect.allowed_extensions_for_file_difference.append(extension)
        else:
            Expect.allowed_extensions_for_file_difference.append("." + extension)

    def __init__(self, actual_value: Any):
        """
        Initializes an Expect object with actual value, owner and logger.

        Args:
            actual_value: The actual value that the assertions will be tested against.
        """
        self._actual_value = actual_value
        self._owner: Optional[object] = None  # Default owner is None
        self._logger = getLogger("Expect")  # Default logger

    def set_owner(self, owner: object):
        """
        Sets the owner for the Expect object.

        Args:
            owner: The object that owns this Expect instance.
        """
        self._owner = owner

    def add_logger(self, logger: Logger):
        """
        Sets the logger for the Expect object.

        Args:
            logger: The Logger to be used for logging.
        """
        self._logger = logger

    @property
    def also(self):
        """
        Property that simply returns self, allowing for more fluent chaining of expectations.

        Returns
        -------
        Expect
            Returns the instance of the Expect class.
        """
        return self

    @expect_logging_helper
    def to_be(self, expected_value):
        """
        Checks if the actual value is equal to the expected value.

        Args:
            expected_value (Any): The expected value.

        Returns:
            bool: True if the actual value is equal to the expected value, False otherwise.
        """
        return self._actual_value == expected_value

    @expect_logging_helper
    def not_to_be(self, expected_value):
        """
        Checks if the actual value is not equal to the expected value.

        Args:
            expected_value (Any): The expected value.

        Returns:
            bool: True if the actual value is not equal to the expected value, False otherwise.
        """
        return self._actual_value != expected_value

    @expect_logging_helper
    def not_to_contain(self, expected_value: str):
        """
        Checks if the actual string value does not contain the expected string.

        Args:
            expected_value (str): The expected string.

        Returns:
            bool: True if the actual string does not contain the expected string, False otherwise.
        """
        return (
            isinstance(self._actual_value, str)
            and expected_value not in self._actual_value
        )

    @expect_logging_helper
    def to_match(self, expected_pattern: str):
        """
        Checks if the actual string value matches the expected regex pattern.

        Args:
            expected_pattern (str): The expected regex pattern.

        Returns:
            bool: True if the actual string matches the expected pattern, False otherwise.
        """
        return (
            isinstance(self._actual_value, str)
            and re.match(expected_pattern, self._actual_value) is not None
        )

    @expect_logging_helper
    def not_to_match(self, expected_pattern: str):
        """
        Checks if the actual string value does not match the expected regex pattern.

        Args:
            expected_pattern (str): The expected regex pattern.

        Returns:
            bool: True if the actual string does not match the expected pattern, False otherwise.
        """
        return (
            isinstance(self._actual_value, str)
            and re.match(expected_pattern, self._actual_value) is None
        )

    @expect_logging_helper
    def to_contain_only_letters(self):
        """
        Checks if the actual string value contains only letters.

        Returns:
            bool: True if the actual string contains only letters, False otherwise.
        """
        return isinstance(self._actual_value, str) and self._actual_value.isalpha()

    @expect_logging_helper
    def not_to_contain_only_letters(self):
        """
        Checks if the actual string value does not contain only letters.

        Returns:
            bool: True if the actual string does not contain only letters, False otherwise.
        """
        return isinstance(self._actual_value, str) and not self._actual_value.isalpha()

    @expect_logging_helper
    def to_contain_only_digits(self):
        """
        Checks if the actual string value contains only digits.

        Returns:
            bool: True if the actual string contains only digits, False otherwise.
        """
        return isinstance(self._actual_value, str) and self._actual_value.isdigit()

    @expect_logging_helper
    def not_to_contain_only_digits(self):
        """
        Checks if the actual string value does not contain only digits.

        Returns:
            bool: True if the actual string does not contain only digits, False otherwise.
        """
        return isinstance(self._actual_value, str) and not self._actual_value.isdigit()

    @expect_logging_helper
    def to_be_lowercase(self):
        """
        Checks if the actual string value is lowercase.

        Returns:
            bool: True if the actual string is lowercase, False otherwise.
        """
        return isinstance(self._actual_value, str) and self._actual_value.islower()

    @expect_logging_helper
    def not_to_be_lowercase(self):
        """
        Checks if the actual string value is not lowercase.

        Returns:
            bool: True if the actual string is not lowercase, False otherwise.
        """
        return isinstance(self._actual_value, str) and not self._actual_value.islower()

    @expect_logging_helper
    def to_be_uppercase(self):
        """
        Checks if the actual string value is uppercase.

        Returns:
            bool: True if the actual string is uppercase, False otherwise.
        """
        return isinstance(self._actual_value, str) and self._actual_value.isupper()

    @expect_logging_helper
    def not_to_be_uppercase(self):
        """
        Checks if the actual string value is not uppercase.

        Returns:
            bool: True if the actual string is not uppercase, False otherwise.
        """
        return isinstance(self._actual_value, str) and not self._actual_value.isupper()

    @expect_logging_helper
    def to_have_length(self, expected_length: int):
        """
        Checks if the actual string value has the expected length.

        Args:
            expected_length (int): The expected length of the string.

        Returns:
            bool: True if the actual string has the expected length, False otherwise.
        """
        return (
            isinstance(self._actual_value, str)
            and len(self._actual_value) == expected_length
        )

    @expect_logging_helper
    def not_to_have_length(self, expected_length: int):
        """
        Checks if the actual string value does not have the expected length.

        Args:
            expected_length (int): The expected length of the string.

        Returns:
            bool: True if the actual string does not have the expected length, False otherwise.
        """
        return (
            isinstance(self._actual_value, str)
            and len(self._actual_value) != expected_length
        )

    @expect_logging_helper
    def to_be_less_than(self, expected_value: int):
        """
        Checks if the actual value is less than the expected value.

        Args:
            expected_value (int): The expected integer value.

        Returns:
            bool: True if the actual value is less than the expected value, False otherwise.
        """
        return self._actual_value < expected_value

    @expect_logging_helper
    def not_to_be_less_than(self, expected_value: int):
        """
        Checks if the actual value is not less than the expected value.

        Args:
            expected_value (int): The expected integer value.

        Returns:
            bool: True if the actual value is not less than the expected value, False otherwise.
        """
        return self._actual_value >= expected_value

    @expect_logging_helper
    def to_be_greater_than(self, expected_value: int):
        """
        Checks if the actual value is greater than the expected value.

        Args:
            expected_value (int): The expected integer value.

        Returns:
            bool: True if the actual value is greater than the expected value, False otherwise.
        """
        return self._actual_value > expected_value

    @expect_logging_helper
    def not_to_be_greater_than(self, expected_value: int):
        """
        Checks if the actual value is not greater than the expected value.

        Args:
            expected_value (int): The expected integer value.

        Returns:
            bool: True if the actual value is not greater than the expected value, False otherwise.
        """
        return self._actual_value <= expected_value

    @expect_logging_helper
    def to_be_less_than_or_equal_to(self, expected_value: int):
        """
        Checks if the actual value is less than or equal to the expected value.

        Args:
            expected_value (int): The expected integer value.

        Returns:
            bool: True if the actual value is less than or equal to the expected value, False otherwise.
        """
        return self._actual_value <= expected_value

    @expect_logging_helper
    def not_to_be_less_than_or_equal_to(self, expected_value: int):
        """
        Checks if the actual value is not less than or equal to the expected value.

        Args:
            expected_value (int): The expected integer value.

        Returns:
            bool: True if the actual value is not less than or equal to the expected value, False otherwise.
        """
        return self._actual_value > expected_value

    @expect_logging_helper
    def to_be_greater_than_or_equal_to(self, expected_value: int):
        """
        Checks if the actual value is greater than or equal to the expected value.

        Args:
            expected_value (int): The expected integer value.

        Returns:
            bool: True if the actual value is greater than or equal to the expected value, False otherwise.
        """
        return self._actual_value >= expected_value

    @expect_logging_helper
    def not_to_be_greater_than_or_equal_to(self, expected_value: int):
        """
        Checks if the actual value is not greater than or equal to the expected value.

        Args:
            expected_value (int): The expected integer value.

        Returns:
            bool: True if the actual value is not greater than or equal to the expected value, False otherwise.
        """
        return self._actual_value < expected_value

    @expect_logging_helper
    def to_be_between(self, lower_bound: int, upper_bound: int):
        """
        Checks if the actual value is between the lower_bound and upper_bound.

        Args:
            lower_bound (int): The lower boundary value.
            upper_bound (int): The upper boundary value.

        Returns:
            bool: True if the actual value is between the two boundaries, False otherwise.
        """
        return lower_bound <= self._actual_value <= upper_bound

    @expect_logging_helper
    def not_to_be_between(self, lower_bound: int, upper_bound: int):
        """
        Checks if the actual value is not between the lower_bound and upper_bound.

        Args:
            lower_bound (int): The lower boundary value.
            upper_bound (int): The upper boundary value.

        Returns:
            bool: True if the actual value is not between the two boundaries, False otherwise.
        """
        return not lower_bound <= self._actual_value <= upper_bound

    @expect_logging_helper
    def to_be_positive(self):
        """
        Checks if the actual value is a positive number.

        Returns:
            bool: True if the actual value is a positive number, False otherwise.
        """
        return self._actual_value > 0

    @expect_logging_helper
    def not_to_be_positive(self):
        """
        Checks if the actual value is not a positive number.

        Returns:
            bool: True if the actual value is not a positive number, False otherwise.
        """
        return self._actual_value <= 0

    @expect_logging_helper
    def to_be_negative(self):
        """
        Checks if the actual value is a negative number.

        Returns:
            bool: True if the actual value is a negative number, False otherwise.
        """
        return self._actual_value < 0

    @expect_logging_helper
    def not_to_be_negative(self):
        """
        Checks if the actual value is not a negative number.

        Returns:
            bool: True if the actual value is not a negative number, False otherwise.
        """
        return self._actual_value >= 0

    @expect_logging_helper
    def to_be_odd(self):
        """
        Checks if the actual value is an odd number.

        Returns:
            bool: True if the actual value is an odd number, False otherwise.
        """
        return self._actual_value % 2 == 1

    @expect_logging_helper
    def not_to_be_odd(self):
        """
        Checks if the actual value is not an odd number.

        Returns:
            bool: True if the actual value is not an odd number, False otherwise.
        """
        return self._actual_value % 2 == 0

    @expect_logging_helper
    def to_be_even(self):
        """
        Checks if the actual value is an even number.

        Returns:
            bool: True if the actual value is an even number, False otherwise.
        """
        return self._actual_value % 2 == 0

    @expect_logging_helper
    def not_to_be_even(self):
        """
        Checks if the actual value is not an even number.

        Returns:
            bool: True if the actual value is not an even number, False otherwise.
        """
        return self._actual_value % 2 == 1

    @expect_logging_helper
    def to_be_equal_to(self, expected_value: str):
        """
        Checks if the actual string is equal to the expected string.

        Args:
            expected_value (str): Expected string value.

        Returns:
            bool: True if the actual string is equal to the expected string, False otherwise.
        """
        return self._actual_value == expected_value

    @expect_logging_helper
    def not_to_be_equal_to(self, expected_value: str):
        """
        Checks if the actual string is not equal to the expected string.

        Args:
            expected_value (str): Expected string value.

        Returns:
            bool: True if the actual string is not equal to the expected string, False otherwise.
        """
        return self._actual_value != expected_value

    @expect_logging_helper
    def to_start_with(self, expected_value: str):
        """
        Checks if the actual string value starts with the expected string.

        Args:
            expected_value (str): The expected string.

        Returns:
            bool: True if the actual string starts with the expected string, False otherwise.
        """
        return isinstance(self._actual_value, str) and self._actual_value.startswith(
            expected_value
        )

    @expect_logging_helper
    def not_to_start_with(self, expected_value: str):
        """
        Checks if the actual string value does not start with the expected string.

        Args:
            expected_value (str): The expected string.

        Returns:
            bool: True if the actual string does not start with the expected string, False otherwise.
        """
        return isinstance(
            self._actual_value, str
        ) and not self._actual_value.startswith(expected_value)

    @expect_logging_helper
    def to_end_with(self, expected_value: str):
        """
        Checks if the actual string value ends with the expected string.

        Args:
            expected_value (str): The expected string.

        Returns:
            bool: True if the actual string ends with the expected string, False otherwise.
        """
        return isinstance(self._actual_value, str) and self._actual_value.endswith(
            expected_value
        )

    @expect_logging_helper
    def not_to_end_with(self, expected_value: str):
        """
        Checks if the actual string value does not end with the expected string.

        Args:
            expected_value (str): The expected string.

        Returns:
            bool: True if the actual string does not end with the expected string, False otherwise.
        """
        return isinstance(self._actual_value, str) and not self._actual_value.endswith(
            expected_value
        )

    @expect_logging_helper
    def to_contain(self, expected_value: str):
        """
        Checks if the actual string value contains the expected string.

        Args:
            expected_value (str): The expected string.

        Returns:
            bool: True if the actual string contains the expected string, False otherwise.
        """
        return (
            isinstance(self._actual_value, str) and expected_value in self._actual_value
        )

    @expect_logging_helper
    def to_be_more_than(self, expected_value: int):
        """
        Asserts that the actual value is more than the expected value.
        """
        return self._actual_value > expected_value

    @expect_logging_helper
    def not_to_be_more_than(self, expected_value: int):
        """
        Asserts that the actual value is not more than the expected value.
        """
        return not self._actual_value > expected_value

    @expect_logging_helper
    def to_be_less_or_equal_to(self, expected_value: int):
        """
        Asserts that the actual value is less than or equal to the expected value.
        """
        return self._actual_value <= expected_value

    @expect_logging_helper
    def not_to_be_less_or_equal_to(self, expected_value: int):
        """
        Asserts that the actual value is not less than or equal to the expected value.
        """
        return not self._actual_value <= expected_value

    @expect_logging_helper
    def to_be_equal_or_more_than(self, expected_value: int):
        """
        Asserts that the actual value is equal to or more than the expected value.
        """
        return self._actual_value >= expected_value

    @expect_logging_helper
    def not_to_be_equal_or_more_than(self, expected_value: int):
        """
        Asserts that the actual value is not equal to or more than the expected value.
        """
        return not self._actual_value >= expected_value

    @expect_logging_helper
    def in_range(self, lower_bound: int, upper_bound: int):
        """
        Asserts that the actual value is within the range of the provided lower and upper bounds.
        """
        return lower_bound <= self._actual_value <= upper_bound

    @expect_logging_helper
    def not_in_range(self, lower_bound: int, upper_bound: int):
        """
        Asserts that the actual value is not within the range of the provided lower and upper bounds.
        """
        return not (lower_bound <= self._actual_value <= upper_bound)

    @expect_logging_helper
    def positive(self):
        """
        Asserts that the actual value is positive.
        """
        return self._actual_value > 0

    @expect_logging_helper
    def not_positive(self):
        """
        Asserts that the actual value is not positive.
        """
        return not self._actual_value > 0

    @expect_logging_helper
    def negative(self):
        """
        Asserts that the actual value is negative.
        """
        return self._actual_value < 0

    @expect_logging_helper
    def not_negative(self):
        """
        Asserts that the actual value is not negative.
        """
        return not self._actual_value < 0

    @expect_logging_helper
    def odd(self):
        """
        Asserts that the actual value is odd.
        """
        return self._actual_value % 2 != 0

    @expect_logging_helper
    def not_odd(self):
        """
        Asserts that the actual value is not odd.
        """
        return not self._actual_value % 2 != 0

    # Array Operations

    @expect_logging_helper
    def contains(self, expected_item: Union[str, Any, Dict[Any, Any]]):
        """
        Verifies if the actual value (string, array-like object, or dictionary-like object) contains the specified item,
        substring, or key-value pairs.

        Args:
            expected_item (Union[str, Any, Dict[Any, Any]]): The item, substring, or dictionary containing the key-value pairs
            that the actual value is expected to contain.

        Returns:
            bool: True if the actual value contains the specified item, substring, or key-value pairs, False otherwise.
        """

        # Check if the actual value is a dictionary
        if isinstance(self._actual_value, dict) and isinstance(expected_item, dict):
            return all(
                item in self._actual_value.items() for item in expected_item.items()
            )

        # Check if the actual value is a string
        if isinstance(self._actual_value, str) and isinstance(expected_item, str):
            return expected_item in self._actual_value

        # Check if the actual value is an array-like object (excluding strings)
        if isinstance(self._actual_value, collections.abc.Sequence) and not isinstance(
            self._actual_value, str
        ):
            return expected_item in self._actual_value

        # Check if the actual value is a list, tuple, or set
        if isinstance(self._actual_value, (list, tuple, set)):
            return expected_item in self._actual_value

        return False

    @expect_logging_helper
    def not_contains_all(self, items: Union[List[Any], Sequence]):
        """
        Verifies if the actual value (an array-like object) does not contain all the provided items.

        If items is a list, it asserts that the actual value does not contain all the items from the list.
        If items is a sequence, it verifies that the actual array does not contain all the specified items.

        Args:
            items (Union[List[Any], Sequence]): The items to check if they are not all contained in the array.

        Returns:
            bool: True if the actual value does not contain all the items, False otherwise.
        """
        if isinstance(items, list) and all(
            isinstance(i, type(self._actual_value)) for i in items
        ):
            return not all(item in self._actual_value for item in items)
        elif isinstance(items, Sequence):
            return not self.contains_all(items, not_an_assertion=True)
        else:
            return False

    @expect_logging_helper
    def contains_at_least_one(self, items: Sequence[Any]):
        """
        Asserts that the actual value (an array-like object) contains at least one of the provided items.

        Args:
            items (Sequence[Any]): The items to check if at least one of them is contained in the array.

        Returns:
            bool: True if the actual value contains at least one of the items, False otherwise.
        """
        if not isinstance(self._actual_value, (list, tuple, set)):
            return False

        if any(item in self._actual_value for item in items):
            return True

        return False

    @expect_logging_helper
    def to_be_ordered(self, expected_items: List[Any]):
        """
        Asserts that the actual value (an array-like object) is the same as the provided list of items in the same order

        Args:
            expected_items (List[Any]): The items to compare with the actual value in terms of both content and order.

        Returns:
            bool: True if the actual value matches the expected list in both content and order, False otherwise.
        """
        return (
            isinstance(self._actual_value, (list, tuple, set))
            and self._actual_value == expected_items
        )

    @expect_logging_helper
    def not_to_be_ordered(self, expected_items: List[Any]):
        """
        Asserts that the actual value (an array-like object) is not the same as the provided list of items in terms of
        order.

        Args:
            expected_items (List[Any]): The items to compare with the actual value in terms of order.

        Returns:
            bool: True if the actual value does not match the expected list in terms of order, False otherwise.
        """
        return (
            isinstance(self._actual_value, (list, tuple, set))
            and self._actual_value != expected_items
        )

    @expect_logging_helper
    def has_key(self, key: Any):
        """
        Asserts that the actual value (a dictionary-like object) contains the expected key.

        Args:
            key (Any): The key to check if it is present in the dictionary.

        Returns:
            bool: True if the actual value contains the key, False otherwise.
        """
        return (
            isinstance(self._actual_value, collections.abc.Mapping)
            and key in self._actual_value
        )

    @expect_logging_helper
    def has_key_value(self, expected_key: Any, expected_value: Any):
        """
        Asserts that the actual value (a dictionary-like object) contains the expected key-value pair.

        Args:
            expected_key (Any): The key to check if it is present in the dictionary.
            expected_value (Any): The value to check if it is associated with the expected key in the dictionary.

        Returns:
            bool: True if the actual value contains the expected key-value pair, False otherwise.
        """
        return (
            isinstance(self._actual_value, dict)
            and self._actual_value.get(expected_key) == expected_value
        )

    @expect_logging_helper
    def not_has_key_value(self, expected_key: Any, expected_value: Any):
        """
        Asserts that the actual value (a dictionary-like object) does not contain the expected key-value pair.

        Args:
            expected_key (Any): The key to check if it is not present in the dictionary.
            expected_value (Any): The value to check if it is not associated with the expected key in the dictionary.

        Returns:
            bool: True if the actual value does not contain the expected key-value pair, False otherwise.
        """
        return (
            isinstance(self._actual_value, dict)
            and self._actual_value.get(expected_key) != expected_value
        )

    @expect_logging_helper
    def has_all_keys(self, expected_keys: Iterable[Any]):
        """
        Asserts that the actual value (a dictionary-like object) contains all the expected keys.

        Args:
            expected_keys (Iterable[Any]): The keys that should be present in the actual value.

        Returns:
            bool: True if the actual value contains all the expected keys, False otherwise.
        """
        return isinstance(self._actual_value, dict) and all(
            key in self._actual_value for key in expected_keys
        )

    @expect_logging_helper
    def not_has_all_keys(self, expected_keys: Iterable[Any]):
        """
        Asserts that the actual value (a dictionary-like object) does not contain all the expected keys.

        Args:
            expected_keys (Iterable[Any]): The keys that should not be present in the actual value altogether.

        Returns:
            bool: True if the actual value does not contain all the expected keys together, False otherwise.
        """
        return isinstance(self._actual_value, dict) and not all(
            key in self._actual_value for key in expected_keys
        )

    @expect_logging_helper
    def has_any_key(self, expected_keys: Iterable[Any]):
        """
        Asserts that the actual value (a dictionary-like object) contains any of the expected keys.

        Args:
            expected_keys (Iterable[Any]): The keys, any of which should be present in the actual value.

        Returns:
            bool: True if the actual value contains any of the expected keys, False otherwise.
        """
        return isinstance(self._actual_value, dict) and any(
            key in self._actual_value for key in expected_keys
        )

    @expect_logging_helper
    def not_has_any_key(self, expected_keys: Iterable[Any]):
        """
        Asserts that the actual value (a dictionary-like object) does not contain any of the expected keys.

        Args:
            expected_keys (Iterable[Any]): The keys, none of which should be present in the actual value.

        Returns:
            bool: True if the actual value does not contain any of the expected keys, False otherwise.
        """
        return isinstance(self._actual_value, dict) and not any(
            key in self._actual_value for key in expected_keys
        )

    @expect_logging_helper
    def is_none(self):
        """
        Verifies if the actual value is None.

        Returns:
            bool: True if the actual value is None, False otherwise.
        """
        return self._actual_value is None

    @expect_logging_helper
    def is_not_none(self):
        """
        Verifies if the actual value is not None.

        Returns:
            bool: True if the actual value is not None, False otherwise.
        """
        return self._actual_value is not None

    @expect_logging_helper
    def is_of_type(self, expected_type):
        """
        Verifies if the actual value is of the expected type.

        Args:
            expected_type (type): The expected type of the actual value.

        Returns:
            bool: True if the actual value is of the expected type, False otherwise.
        """
        return isinstance(self._actual_value, expected_type)

    @expect_logging_helper
    def is_not_of_type(self, unexpected_type):
        """
        Verifies if the actual value is not of the unexpected type.

        Args:
            unexpected_type (type): The type that the actual value should not be.

        Returns:
            bool: True if the actual value is not of the unexpected type, False otherwise.
        """
        return not isinstance(self._actual_value, unexpected_type)

    @expect_logging_helper
    def has_size(self, expected_size):
        """
        Verifies if the actual value (expected to be a collection) has the expected size.

        Args:
            expected_size (int): The expected size of the collection.

        Returns:
            bool: True if the actual value has the expected size, False otherwise.
        """
        return len(self._actual_value) == expected_size

    @expect_logging_helper
    def is_empty(self):
        """
        Verifies if the actual value (expected to be a collection) is empty.

        Returns:
            bool: True if the actual value is empty, False otherwise.
        """
        return len(self._actual_value) == 0

    @expect_logging_helper
    def is_truthy(self):
        """
        Verifies if the actual value is truthy (not None, not False, not zero, and not an empty collection).

        Returns:
            bool: True if the actual value is truthy, False otherwise.
        """
        return bool(self._actual_value)

    @expect_logging_helper
    def is_falsy(self):
        """
        Verifies if the actual value is falsy (None, False, zero, or an empty collection).

        Returns:
            bool: True if the actual value is falsy, False otherwise.
        """
        return not bool(self._actual_value)

    @expect_logging_helper
    def is_in(self, collection):
        """
        Verifies if the actual value is present in the given collection.

        Args:
            collection (iterable): The collection in which to look for the actual value.

        Returns:
            bool: True if the actual value is in the collection, False otherwise.
        """
        return self._actual_value in collection

    @expect_logging_helper
    def is_not_in(self, collection):
        """
        Verifies if the actual value is not present in the given collection.

        Args:
            collection (iterable): The collection in which to look for the actual value.

        Returns:
            bool: True if the actual value is not in the collection, False otherwise.
        """
        return self._actual_value not in collection

    @expect_logging_helper
    def starts_with(self, prefix: str):
        """
        Verifies if the actual string starts with the specified prefix.

        Args:
            prefix (str): The prefix that the actual string is expected to start with.

        Returns:
            bool: True if the actual string starts with the prefix, False otherwise.
        """
        if isinstance(self._actual_value, str):
            return self._actual_value.startswith(prefix)
        else:
            return False

    @expect_logging_helper
    def ends_with(self, suffix: str):
        """
        Verifies if the actual string ends with the specified suffix.

        Args:
            suffix (str): The suffix that the actual string is expected to end with.

        Returns:
            bool: True if the actual string ends with the suffix, False otherwise.
        """
        if isinstance(self._actual_value, str):
            return self._actual_value.endswith(suffix)
        else:
            return False

    @expect_logging_helper
    def matches(self, pattern: str):
        """
        Verifies if the actual string matches the specified regex pattern.

        Args:
            pattern (str): The regex pattern that the actual string is expected to match.

        Returns:
            bool: True if the actual string matches the pattern, False otherwise.
        """
        if isinstance(self._actual_value, str):
            return re.match(pattern, self._actual_value) is not None
        else:
            return False

    # Implement not versions for string methods
    @expect_logging_helper
    def not_starts_with(self, prefix: str):
        """
        Verifies if the actual string does not start with the specified prefix.

        Args:
            prefix (str): The prefix that the actual string is not expected to start with.

        Returns:
            bool: True if the actual string does not start with the prefix, False otherwise.
        """
        return not self.starts_with(prefix, not_an_assertion=True)

    @expect_logging_helper
    def not_ends_with(self, suffix: str):
        """
        Verifies if the actual string does not end with the specified suffix.

        Args:
            suffix (str): The suffix that the actual string is not expected to end with.

        Returns:
            bool: True if the actual string does not end with the suffix, False otherwise.
        """
        return not self.ends_with(suffix, not_an_assertion=True)

    @expect_logging_helper
    def not_contains(self, substring: str):
        """
        Verifies if the actual string does not contain the specified substring.

        Args:
            substring (str): The substring that the actual string is not expected to contain.

        Returns:
            bool: True if the actual string does not contain the substring, False otherwise.
        """
        return not self.contains(substring, not_an_assertion=True)

    @expect_logging_helper
    def not_matches(self, pattern: str):
        """
        Verifies if the actual string does not match the specified regex pattern.

        Args:
            pattern (str): The regex pattern that the actual string is not expected to match.

        Returns:
            bool: True if the actual string does not match the pattern, False otherwise.
        """
        return not self.matches(pattern, not_an_assertion=True)

    @expect_logging_helper
    def has_same_items(self, expected_value: Sequence):
        """
        Verifies if the actual array has the same items as the expected array, regardless of order.

        Args:
            expected_value (Sequence): The array that the actual array is expected to have the same items as.

        Returns:
            bool: True if the actual array has the same items as the expected array, False otherwise.
        """
        if isinstance(self._actual_value, collections.abc.Sequence) and not isinstance(
            self._actual_value, str
        ):
            return sorted(self._actual_value) == sorted(expected_value)
        else:
            return False

    @expect_logging_helper
    def contains_all(self, items: Sequence[Any]):
        """
        Verifies if the actual array contains all the specified items, regardless of order.

        Args:
            items (Sequence[Any]): The items that the actual array is expected to contain.

        Returns:
            bool: True if the actual array contains all the items, False otherwise.
        """
        if isinstance(self._actual_value, collections.abc.Sequence) and not isinstance(
            self._actual_value, str
        ):
            return all(item in self._actual_value for item in items)

        return False

    @expect_logging_helper
    def is_ordered(self, expected_value: Sequence):
        """
        Verifies if the actual array is in the same order as the expected array.

        Args:
            expected_value (Sequence): The array that defines the expected order of the actual array.

        Returns:
            bool: True if the actual array is in the same order as the expected array, False otherwise.
        """
        if isinstance(self._actual_value, collections.abc.Sequence) and not isinstance(
            self._actual_value, str
        ):
            return self._actual_value == expected_value
        else:
            return False

    # Implement not versions for array methods
    @expect_logging_helper
    def not_has_same_items(self, expected_value: Sequence):
        """
        Verifies if the actual array does not have the same items as the expected array, regardless of order.

        Args:
            expected_value (Sequence): The array that the actual array is not expected to have the same items as.

        Returns:
            bool: True if the actual array does not have the same items as the expected array, False otherwise.
        """
        return not self.has_same_items(expected_value, not_an_assertion=True)

    @expect_logging_helper
    def not_contains_at_least_one(self, items: Sequence[Any]):
        """
        Asserts that the actual value (an array-like object) does not contain any of the provided items.

        Args:
            items (Sequence[Any]): The items to check if none of them are contained in the array.

        Returns:
            bool: True if the actual value does not contain any of the items, False otherwise.
        """
        if not isinstance(self._actual_value, (list, tuple, set)):
            return False

        if all(item not in self._actual_value for item in items):
            return True

        return False

    @expect_logging_helper
    def not_is_ordered(self, expected_value: Sequence):
        """
        Verifies if the actual array is not in the same order as the expected array.

        Args:
            expected_value (Sequence): The array that defines the order that the actual array is not expected to have.

        Returns:
            bool: True if the actual array is not in the same order as the expected array, False otherwise.
        """
        return not self.is_ordered(expected_value, not_an_assertion=True)

    @expect_logging_helper
    def has_value(self, value: Any):
        """
        Verifies if the actual dictionary contains the specified value.

        Args:
            value (Any): The value that the actual dictionary is expected to contain.

        Returns:
            bool: True if the actual dictionary contains the value, False otherwise.
        """
        if isinstance(self._actual_value, collections.abc.Mapping):
            return value in self._actual_value.values()
        else:
            return False

    @expect_logging_helper
    def has_item(self, key: Any, value: Any):
        """
        Verifies if the actual dictionary contains the specified key-value pair.

        Args:
            key (Any): The key of the key-value pair that the actual dictionary is expected to contain.
            value (Any): The value of the key-value pair that the actual dictionary is expected to contain.

        Returns:
            bool: True if the actual dictionary contains the key-value pair, False otherwise.
        """
        if isinstance(self._actual_value, collections.abc.Mapping):
            return self._actual_value.get(key) == value
        else:
            return False

    @expect_logging_helper
    def not_has_key(self, key: Any):
        """
        Asserts that the actual value (a dictionary-like object) does not contain the expected key.

        Args:
            key (Any): The key to check if it is not present in the dictionary.

        Returns:
            bool: True if the actual value does not contain the key, False otherwise.
        """
        return (
            isinstance(self._actual_value, collections.abc.Mapping)
            and key not in self._actual_value
        )

    @expect_logging_helper
    def not_has_value(self, value: Any):
        """
        Verifies if the actual dictionary does not contain the specified value.

        Args:
            value (Any): The value that the actual dictionary is not expected to contain.

        Returns:
            bool: True if the actual dictionary does not contain the value, False otherwise.
        """
        return not self.has_value(value, not_an_assertion=True)

    @expect_logging_helper
    def not_has_item(self, key: Any, value: Any):
        """
        Verifies if the actual dictionary does not contain the specified key-value pair.

        Args:
            key (Any): The key of the key-value pair that the actual dictionary is not expected to contain.
            value (Any): The value of the key-value pair that the actual dictionary is not expected to contain.

        Returns:
            bool: True if the actual dictionary does not contain the key-value pair, False otherwise.
        """
        return not self.has_item(key, value, not_an_assertion=True)

    @expect_logging_helper
    def to_be_before(self, other_date: datetime.datetime) -> "Expect":
        """
        Check if the actual date is before the other date.

        Args:
            other_date (datetime.datetime): The date that the actual date should be before.

        Returns:
            Expect: The Expect instance for chain calls.
        """
        return self._actual_value < other_date

    @expect_logging_helper
    def to_be_after(self, other_date: datetime.datetime) -> "Expect":
        """
        Check if the actual date is after the other date.

        Args:
            other_date (datetime.datetime): The date that the actual date should be after.

        Returns:
            Expect: The Expect instance for chain calls.
        """
        return self._actual_value > other_date

    @expect_logging_helper
    def to_have_year(self, year: int) -> "Expect":
        """
        Check if the actual date has the specified year.

        Args:
            year (int): The year that the actual date should have.

        Returns:
            Expect: The Expect instance for chain calls.
        """
        return self._actual_value.year == year

    @expect_logging_helper
    def to_have_month(self, month: int) -> "Expect":
        """
        Check if the actual date has the specified month.

        Args:
            month (int): The month that the actual date should have.

        Returns:
            Expect: The Expect instance for chain calls.
        """
        return self._actual_value.month == month

    @expect_logging_helper
    def to_have_day(self, day: int) -> "Expect":
        """
        Check if the actual date has the specified day.

        Args:
            day (int): The day that the actual date should have.

        Returns:
            Expect: The Expect instance for chain calls.
        """
        return self._actual_value.day == day

    @expect_logging_helper
    def to_have_hour(self, hour: int) -> "Expect":
        """
        Check if the actual date has the specified hour.

        Args:
            hour (int): The hour that the actual date should have.

        Returns:
            Expect: The Expect instance for chain calls.
        """
        return self._actual_value.hour == hour

    @expect_logging_helper
    def to_have_minute(self, minute: int) -> "Expect":
        """
        Check if the actual date has the specified minute.

        Args:
            minute (int): The minute that the actual date should have.

        Returns:
            Expect: The Expect instance for chain calls.
        """
        return self._actual_value.minute == minute

    @expect_logging_helper
    def to_have_second(self, second: int) -> "Expect":
        """
        Check if the actual date has the specified second.

        Args:
            second (int): The second that the actual date should have.

        Returns:
            Expect: The Expect instance for chain calls.
        """
        return self._actual_value.second == second

    @expect_logging_helper
    def not_to_be_before(
        self,
        other_datetime: datetime.datetime,
        not_an_assertion: Optional[bool] = False,
    ):
        """
        Checks if the actual value is not before the expected datetime.

        Args:
            other_datetime (datetime): The datetime to compare with the actual value.
            not_an_assertion (bool, optional): Whether this is not an assertion (default: False).

        Returns:
            Expect: The Expect instance with the result of the check.
        """
        return self._actual_value >= other_datetime

    @expect_logging_helper
    def not_to_be_after(
        self,
        other_datetime: datetime.datetime,
        not_an_assertion: Optional[bool] = False,
    ):
        """
        Checks if the actual value is not after the expected datetime.

        Args:
            other_datetime (datetime): The datetime to compare with the actual value.
            not_an_assertion (bool, optional): Whether this is not an assertion (default: False).

        Returns:
            Expect: The Expect instance with the result of the check.
        """
        return self._actual_value <= other_datetime

    @expect_logging_helper
    def not_to_be_on_or_before(
        self,
        other_datetime: datetime.datetime,
        not_an_assertion: Optional[bool] = False,
    ):
        """
        Checks if the actual value is not on or before the expected datetime.

        Args:
            other_datetime (datetime): The datetime to compare with the actual value.
            not_an_assertion (bool, optional): Whether this is not an assertion (default: False).

        Returns:
            Expect: The Expect instance with the result of the check.
        """
        return self._actual_value > other_datetime

    @expect_logging_helper
    def not_to_be_on_or_after(
        self,
        other_datetime: datetime.datetime,
        not_an_assertion: Optional[bool] = False,
    ):
        """
        Checks if the actual value is not on or after the expected datetime.

        Args:
            other_datetime (datetime): The datetime to compare with the actual value.
            not_an_assertion (bool, optional): Whether this is not an assertion (default: False).

        Returns:
            Expect: The Expect instance with the result of the check.
        """
        return self._actual_value < other_datetime

    @expect_logging_helper
    def not_to_be_within_delta(
        self,
        other_datetime: Union[datetime.datetime, float, int],
        delta: Union[timedelta, float, int],
    ):
        """
        Checks if the actual value is not within a certain delta of an expected value.

        Args:
            other_datetime (Union[datetime, float, int]): The datetime, float or integer to compare with the actual value.
            delta (Union[timedelta, float, int]): The timedelta, float or integer to use for the comparison.

        Returns:
            Expect: The Expect instance with the result of the check.
        """
        if isinstance(other_datetime, datetime.datetime) and isinstance(
            delta, timedelta
        ):
            lower_bound = other_datetime - delta
            upper_bound = other_datetime + delta
            return not lower_bound <= self._actual_value <= upper_bound
        else:
            difference = abs(self._actual_value - other_datetime)
            return difference > delta

    @expect_logging_helper
    def to_be_within_delta(self, expected_value, delta):
        """
        Checks if the actual value is within a certain delta of an expected value.

        Args:
            expected_value (Union[int, float, datetime]): The expected value.
            delta (Union[int, float, timedelta]): The allowed difference.

        Returns:
            bool: True if the actual value is within the delta of the expected value, False otherwise.
        """
        if isinstance(self._actual_value, datetime):
            return abs(self._actual_value - expected_value) <= delta
        return abs(self._actual_value - expected_value) <= delta

    @expect_logging_helper
    def to_be_in_range_with_delta(self, start_value, end_value, delta):
        """
        Checks if the actual value is within a certain range plus-minus a delta.

        Args:
            start_value (Union[int, float, datetime]): The start of the range.
            end_value (Union[int, float, datetime]): The end of the range.
            delta (Union[int, float, timedelta]): The allowed difference.

        Returns:
            bool: True if the actual value is within the range plus-minus the delta, False otherwise.
        """
        return start_value - delta <= self._actual_value <= end_value + delta

    @expect_logging_helper
    def not_to_be_in_range_with_delta(self, start_value, end_value, delta):
        """
        Checks if the actual value is not within a certain range plus-minus a delta.

        Args:
            start_value (Union[int, float, datetime]): The start of the range.
            end_value (Union[int, float, datetime]): The end of the range.
            delta (Union[int, float, timedelta]): The allowed difference.

        Returns:
            bool: True if the actual value is not within the range plus-minus the delta, False otherwise.
        """
        return not self.to_be_in_range_with_delta(start_value, end_value, delta)

    @expect_logging_helper
    def to_be_equal_with_threshold(self, expected_value, threshold):
        """
        Checks if the actual value is equal to an expected value within a certain threshold.

        Args:
            expected_value (Union[int, float, datetime]): The expected value.
            threshold (Union[int, float, timedelta]): The allowed difference.

        Returns:
            bool: True if the actual value is equal to the expected value within the threshold, False otherwise.
        """
        return abs(self._actual_value - expected_value) <= threshold

    @expect_logging_helper
    def not_to_be_equal_with_threshold(self, expected_value, threshold):
        """
        Checks if the actual value is not equal to an expected value within a certain threshold.

        Args:
            expected_value (Union[int, float, datetime]): The expected value.
            threshold (Union[int, float, timedelta]): The allowed difference.

        Returns:
            bool: True if the actual value is not equal to the expected value within the threshold, False otherwise.
        """
        return not self.to_be_equal_with_threshold(expected_value, threshold)

    @expect_logging_helper
    def to_be_file(self):
        """
        Checks if the actual value is a file.

        Returns:
            bool: True if the actual value is a file, False otherwise.
        """
        return os.path.isfile(self._actual_value)

    @expect_logging_helper
    def not_to_be_file(self):
        """
        Checks if the actual value is not a file.

        Returns:
            bool: True if the actual value is not a file, False otherwise.
        """
        return not self.to_be_file()

    @expect_logging_helper
    def to_be_directory(self):
        """
        Checks if the actual value is a directory.

        Returns:
            bool: True if the actual value is a directory, False otherwise.
        """
        return os.path.isdir(self._actual_value)

    @expect_logging_helper
    def not_to_be_directory(self):
        """
        Checks if the actual value is not a directory.

        Returns:
            bool: True if the actual value is not a directory, False otherwise.
        """
        return not self.to_be_directory()

    @expect_logging_helper
    def to_exist(self):
        """
        Checks if the actual value exists.

        Returns:
            bool: True if the actual value exists, False otherwise.
        """
        return os.path.exists(self._actual_value)

    @expect_logging_helper
    def not_to_exist(self):
        """
        Checks if the actual value does not exist.

        Returns:
            bool: True if the actual value does not exist, False otherwise.
        """
        return not self.to_exist()

    @expect_logging_helper
    def to_be_readable(self):
        """
        Checks if the actual value is readable.

        Returns:
            bool: True if the actual value is readable, False otherwise.
        """
        return os.access(self._actual_value, os.R_OK)

    @expect_logging_helper
    def not_to_be_readable(self):
        """
        Checks if the actual value is not readable.

        Returns:
            bool: True if the actual value is not readable, False otherwise.
        """
        return not self.to_be_readable()

    @expect_logging_helper
    def to_be_writable(self):
        """
        Checks if the actual value is writable.

        Returns:
            bool: True if the actual value is writable, False otherwise.
        """
        return os.access(self._actual_value, os.W_OK)

    @expect_logging_helper
    def not_to_be_writable(self):
        """
        Checks if the actual value is not writable.

        Returns:
            bool: True if the actual value is not writable, False otherwise.
        """
        return not self.to_be_writable()

    @expect_logging_helper
    def to_have_extension(self, expected_extension):
        """
        Checks if the actual value has a specific extension.

        Args:
            expected_extension (str): The expected extension.

        Returns:
            bool: True if the actual value has the expected extension, False otherwise.
        """
        _, extension = os.path.splitext(self._actual_value)
        return extension.lower() == expected_extension.lower()

    @expect_logging_helper
    def not_to_have_extension(self, expected_extension):
        """
        Checks if the actual value does not have a specific extension.

        Args:
            expected_extension (str): The expected extension.

        Returns:
            bool: True if the actual value does not have the expected extension, False otherwise.
        """
        return not self.to_have_extension(expected_extension)

    @expect_logging_helper
    def size_to_be_within_range(self, min_size, max_size):
        """
        Checks if the size of the actual value is within a certain range.

        Args:
            min_size (int): The minimum size.
            max_size (int): The maximum size.

        Returns:
            bool: True if the size of the actual value is within the specified range, False otherwise.
        """
        size = os.path.getsize(self._actual_value)
        return min_size <= size <= max_size

    @expect_logging_helper
    def size_not_to_be_within_range(self, min_size, max_size):
        """
        Checks if the size of the actual value is not within a certain range.

        Args:
            min_size (int): The minimum size.
            max_size (int): The maximum size.

        Returns:
            bool: True if the size of the actual value is not within the specified range, False otherwise.
        """
        return not self.size_to_be_within_range(min_size, max_size)

    @expect_logging_helper
    def to_have_permission(self, permission):
        """
        Checks if the actual value has a specific permission.

        Args:
            permission (str): The expected permission. This can be 'r' for readable, 'w' for writable, and 'x' for
            executable.

        Returns:
            bool: True if the actual value has the expected permission, False otherwise.
        """
        permissions = {"r": os.R_OK, "w": os.W_OK, "x": os.X_OK}
        return os.access(self._actual_value, permissions[permission.lower()])

    @expect_logging_helper
    def not_to_have_permission(self, permission):
        """
        Checks if the actual value does not have a specific permission.

        Args:
            permission (str): The expected permission. This can be 'r' for readable, 'w' for writable, and 'x' for
            executable.

        Returns:
            bool: True if the actual value does not have the expected permission, False otherwise.
        """
        return not self.to_have_permission(permission)

    @expect_logging_helper
    def to_be_of_size(self, size):
        """
        Checks if the actual value has a specific size.

        Args:
            size (int): The expected size in bytes.

        Returns:
            bool: True if the actual value has the expected size, False otherwise.
        """
        return os.path.getsize(self._actual_value) == size

    @expect_logging_helper
    def not_to_be_of_size(self, size):
        """
        Checks if the actual value does not have a specific size.

        Args:
            size (int): The expected size in bytes.

        Returns:
            bool: True if the actual value does not have the expected size, False otherwise.
        """
        return not self.to_be_of_size(size)

    @expect_logging_helper
    def to_be_empty(self):
        """
        Checks if the actual value is an empty directory or an empty file.

        Returns:
            bool: True if the actual value is an empty directory or an empty file, False otherwise.
        """
        if os.path.isdir(self._actual_value):
            return not os.listdir(self._actual_value)
        elif os.path.isfile(self._actual_value):
            return os.path.getsize(self._actual_value) == 0
        else:
            return False

    @expect_logging_helper
    def not_to_be_empty(self):
        """
        Checks if the actual value is not an empty directory.

        Returns:
            bool: True if the actual value is not an empty directory, False otherwise.
        """
        return not self.to_be_empty(not_an_assertion=True)

    @expect_logging_helper
    def to_be_modified_within(self, seconds):
        """
        Checks if the actual value was modified within a certain time.

        Args:
            seconds (int): The expected time in seconds.

        Returns:
            bool: True if the actual value was modified within the expected time, False otherwise.
        """
        return time.time() - os.path.getmtime(self._actual_value) <= seconds

    @expect_logging_helper
    def not_to_be_modified_within(self, seconds):
        """
        Checks if the actual value was not modified within a certain time.

        Args:
            seconds (int): The expected time in seconds.

        Returns:
            bool: True if the actual value was not modified within the expected time, False otherwise.
        """
        return not self.to_be_modified_within(seconds)

    @expect_logging_helper
    def to_be_symlink(self):
        """
        Checks if the actual value is a symlink.

        Returns:
            bool: True if the actual value is a symlink, False otherwise.
        """
        return os.path.islink(self._actual_value)

    @expect_logging_helper
    def not_to_be_symlink(self):
        """
        Checks if the actual value is not a symlink.

        Returns:
            bool: True if the actual value is not a symlink, False otherwise.
        """
        return not self.to_be_symlink()

    @expect_logging_helper
    def to_be_absolute_path(self):
        """
        Checks if the actual value is an absolute path.

        Returns:
            bool: True if the actual value is an absolute path, False otherwise.
        """
        return os.path.isabs(self._actual_value)

    @expect_logging_helper
    def not_to_be_absolute_path(self):
        """
        Checks if the actual value is not an absolute path.

        Returns:
            bool: True if the actual value is not an absolute path, False otherwise.
        """
        return not self.to_be_absolute_path()

    @expect_logging_helper
    def to_be_identical_with(self, comparison_value):
        """
        Check whether the `_actual_value` is identical with the provided comparison_value.

        This method treats files and strings. If the actual value or the comparison value is a path to a file,
        it reads the file content and makes the comparison.

        :param comparison_value: The value to be compared with. It could be a string or a path to a text file.
        :return: True if the actual value is identical with the comparison_value, False otherwise.
        """
        actual = self._actual_value
        if os.path.isfile(self._actual_value):
            with open(self._actual_value, "r") as f:
                actual = f.read()

        if os.path.isfile(comparison_value):
            with open(comparison_value, "r") as f:
                comparison_value = f.read()

        return actual == comparison_value

    @expect_logging_helper
    def not_to_be_identical_with(self, comparison_value):
        """
        Check whether the `_actual_value` is not identical with the provided comparison_value.

        This method treats files and strings. If the actual value or the comparison value is a path to a file,
        it reads the file content and makes the comparison.

        :param comparison_value: The value to be compared with. It could be a string or a path to a text file.
        :return: True if the actual value is not identical with the comparison_value, False otherwise.
        """
        return not self.to_be_identical_with(comparison_value)

    def _log_results(
        self,
        result: bool,
        method: str,
        e_args: tuple,
        e_kwargs: dict,
        is_assertion: bool,
    ):
        """
        Logs the result of the test.

        Args:
            result (bool): The result of the test.
            method (str): The name of the method that performed the test.
            e_args (tuple): The positional arguments that were passed to the method.
            e_kwargs (dict): The keyword arguments that were passed to the method.
            is_assertion (bool): Whether this is an assertion (True) or a verification (False).
        """
        message = self._build_message(result, method, is_assertion, e_args, e_kwargs)

        extra = {"assertion": result} if is_assertion else {}

        if result:
            return self._logger.info(message, extra=extra)

        if is_assertion:
            self._logger.critical(message, extra=extra)
            raise Exception(message)

        # finally simply log verification
        self._logger.info(message)

    def _build_message(self, result, method_name, is_assertion, e_args, e_kwargs):
        """
        Builds a log message based on the test result and other information.

        Args:
            result (bool): The result of the test.
            method_name (str): The name of the method that performed the test.
            is_assertion (bool): Whether this is an assertion (True) or a verification (False).
            e_args (tuple): The positional arguments that were passed to the method.
            e_kwargs (dict): The keyword arguments that were passed to the method.

        Returns:
            str: The log message.
        """
        readable_name = method_name.replace("_", " ")
        action = "Assertion" if is_assertion else "Verification"
        status = "Pass" if result else "Fail"
        if self._owner:
            message = (
                f"[{self.owner.__full_name__}] {action} {readable_name}: {status}."
                f"\nActual value: \n{self._actual_value}"
            )
        else:
            message = f"{action} {readable_name}: {status}. \nActual value: \n{self._actual_value}"

        if result:
            return message

        message += self._build_expected_value_using_expectation_args(
            method_name, e_kwargs
        )

        if not self._has_diff():
            return message

        return message + self._build_diff(e_args, e_kwargs)

    def _build_expected_value_using_expectation_args(self, method_name, e_kwargs):
        """
        Constructs the expected value portion of the message based on the method name and provided arguments.

        It dynamically determines which helper function to call for building the message
        based on the data type of the expected value or the presence of "file" in the method name.

        Parameters:
            method_name (str): The name of the method called for expectation.
            e_kwargs (dict): The keyword arguments passed to the method.

        Returns:
            str: The expected value message for the assertion or verification.

        Raises:
            Exception: If unable to build the expected value message for provided arguments.
        """
        # Evaluate the method_name and data type of e_args to determine which helper method to call
        if method_name.lower().find("file") != -1:
            return self._build_file_expected(method_name, e_kwargs)
        elif isinstance(e_kwargs["expected_value"], str):
            return self._build_string_expected(method_name, e_kwargs)
        elif isinstance(e_kwargs["expected_value"], (int, float)):
            return self._build_numeric_expected(method_name, e_kwargs)
        elif isinstance(e_kwargs["expected_value"], list):
            return self._build_list_expected(method_name, e_kwargs)
        elif isinstance(e_kwargs["expected_value"], dict):
            return self._build_dict_expected(method_name, e_kwargs)
        elif isinstance(e_kwargs["expected_value"], datetime.datetime):
            return self._build_datetime_expected(method_name, e_kwargs)
        else:
            raise Exception(
                "Unable to build expected value message for provided expectation args."
            )

    @staticmethod
    def _build_string_expected(method_name, kwargs):
        """
        Constructs the expected value message for string based assertions or verifications.

        Parameters:
            method_name (str): The name of the method called for expectation.
            kwargs (dict): The keyword arguments passed to the method.

        Returns:
            str: The expected value message for the string assertion or verification.
        """
        if method_name in [
            "to_be",
            "not_to_be",
            "starts_with",
            "not_starts_with",
            "ends_with",
            "not_ends_with",
            "contains",
            "not_contains",
        ]:
            return f"\nExpected value: \n{kwargs['expected_value']}"
        elif method_name in ["match", "not_match"]:
            return f"\nExpected pattern: \n{kwargs['pattern']}"
        else:
            return f"\nExpected value: \n{kwargs['expected_value']}"

    @staticmethod
    def _build_numeric_expected(method_name, kwargs):
        """
        Build and return the expected value string for numeric methods based on
        the method name and kwargs.
        """
        if method_name in ["to_be", "not_to_be"]:
            return f"\nExpected value: \n{kwargs.get('expected_value', '')}"
        if method_name in [
            "greater_than",
            "not_greater_than",
            "less_than",
            "not_less_than",
        ]:
            return f"\nExpected value: \n{kwargs.get('comparison_value', '')}"
        if method_name in ["in_range", "not_in_range"]:
            return f"\nExpected range: \n{kwargs.get('start', '')} - {kwargs.get('end', '')}"
        if method_name in ["is_positive", "is_not_positive"]:
            return f"\nExpectation: Value should be {'positive' if method_name == 'is_positive' else 'non-positive'}"
        if method_name in ["is_negative", "is_not_negative"]:
            return f"\nExpectation: Value should be {'negative' if method_name == 'is_negative' else 'non-negative'}"
        if method_name in ["is_odd", "is_not_odd"]:
            return f"\nExpectation: Value should be {'odd' if method_name == 'is_odd' else 'even'}"
        if method_name in ["is_even", "is_not_even"]:
            return f"\nExpectation: Value should be {'even' if method_name == 'is_even' else 'odd'}"
        return f'\nExpected value: \n{kwargs.get("expected_value", "")}'

    @staticmethod
    def _build_list_expected(method_name, kwargs):
        """
        Build and return the expected value string for list methods based on
        the method name and kwargs.
        """
        if method_name in ["to_be", "not_to_be"]:
            return f"\nExpected value: \n{kwargs.get('expected_value', '')}"
        if method_name in ["contains", "not_contains"]:
            return f"\nExpected items: \n{kwargs.get('items', '')}"
        if method_name in ["contain_only", "not_contain_only"]:
            return f"\nExpected items only: \n{kwargs.get('items', '')}"
        return f'\nExpected value: \n{kwargs.get("expected_value", "")}'

    @staticmethod
    def _build_dict_expected(method_name, kwargs):
        """
        Build and return the expected value string for dictionary methods based
        on the method name and kwargs.
        """
        if method_name in ["to_be", "not_to_be"]:
            return f"\nExpected value: \n{kwargs.get('expected_value', '')}"
        if method_name in ["contains_keys", "not_contains_keys"]:
            return f"\nExpected keys: \n{kwargs.get('keys', '')}"
        if method_name in ["contains_items", "not_contains_items"]:
            return f"\nExpected items: \n{kwargs.get('items', '')}"
        if method_name in ["contains_values", "not_contains_values"]:
            return f"\nExpected values: \n{kwargs.get('values', '')}"
        return f'\nExpected value: \n{kwargs.get("expected_value", "")}'

    @staticmethod
    def _build_datetime_expected(method_name, kwargs):
        """
        Build and return the expected value string for datetime methods based
        on the method name and kwargs.
        """
        if method_name in ["to_be", "not_to_be"]:
            return f"\nExpected value: \n{kwargs.get('expected_value', '')}"
        if method_name in ["to_be_within_range", "not_to_be_within_range"]:
            return f"\nExpected range: \n{kwargs.get('start', '')} - {kwargs.get('end', '')}"
        if method_name in [
            "to_be_before",
            "not_to_be_before",
            "to_be_after",
            "not_to_be_after",
        ]:
            return f"\nExpected date: \n{kwargs.get('date', '')}"
        return f'\nExpected value: \n{kwargs.get("expected_value", "")}'

    @staticmethod
    def _build_file_expected(method_name, kwargs):
        """
        Build and return the expected value string for file methods based
        on the method name and kwargs.
        """
        expected_file = kwargs.get("file_path", "")
        file_type = "binary" if kwargs.get("binary", False) else "text"
        encoding = kwargs.get("encoding", "utf-8")

        if method_name in ["to_be", "not_to_be"]:
            return f"\nExpected file: \nPath: {expected_file}\nType: {file_type}\nEncoding: {encoding}"

        # Any other method-specific message builders would go here...

        # Default case:
        return f"\nExpected file: \nPath: {expected_file}\nType: {file_type}\nEncoding: {encoding}"

    def _has_diff(self):
        return isinstance(
            self._actual_value, (str, list, dict, int, float, datetime.datetime)
        )

    def _build_diff(self, e_args, e_kwargs):
        """
        Build the difference string based on the type of the actual value.

        Args:
            e_args: The expected arguments passed to the method.
            e_kwargs: The keyword arguments passed to the method.

        Returns:
            A string detailing the difference.
        """

        # Handle case of 0 or 2+ arguments
        if len(e_args) != 1:
            return ""

        expected_value = e_args[0]

        if isinstance(self._actual_value, str):
            diff = difflib.ndiff(self._actual_value, expected_value)
            return "\nString difference:\n" + "\n".join(diff)

        if isinstance(self._actual_value, list):
            return self._list_difference(expected_value)

        if isinstance(self._actual_value, dict):
            return self._dict_difference(expected_value)

        if isinstance(self._actual_value, (int, float)):
            return self._numeric_difference(expected_value)

        if isinstance(self._actual_value, datetime.datetime):
            return self._datetime_difference(expected_value)

        # Placeholder for handling files
        if isinstance(self._actual_value, str) and "file" in self._method_name:
            return self._file_difference(expected_value)

        # When we don't know how to generate a diff, return an empty string.
        return ""

    def _list_difference(self, expected_value):
        """
        Build the difference string for lists.

        Args:
            expected_value: The expected value to compare with.

        Returns:
            A string detailing the difference.
        """
        extra_items = [i for i in self._actual_value if i not in expected_value]
        missing_items = [i for i in expected_value if i not in self._actual_value]

        diff_message = ""
        if extra_items:
            diff_message += "\nExtra items in actual value: " + ", ".join(
                map(str, extra_items)
            )
        if missing_items:
            diff_message += "\nItems missing in actual value: " + ", ".join(
                map(str, missing_items)
            )

        return diff_message

    def _dict_difference(self, expected_value):
        """
        Build the difference string for dictionaries.

        Args:
            expected_value: The expected value to compare with.

        Returns:
            A string detailing the difference.
        """
        extra_keys = set(self._actual_value.keys()) - set(expected_value.keys())
        missing_keys = set(expected_value.keys()) - set(self._actual_value.keys())

        diff_message = ""
        if extra_keys:
            diff_message += "\nExtra keys in actual value: " + ", ".join(extra_keys)
        if missing_keys:
            diff_message += "\nKeys missing in actual value: " + ", ".join(missing_keys)

        for key in self._actual_value:
            if key in expected_value and self._actual_value[key] != expected_value[key]:
                diff_message += (
                    f"\nFor key '{key}': actual value is '{self._actual_value[key]}', expected value is"
                    f" '{expected_value[key]}'"
                )

        return diff_message

    def _datetime_difference(self, expected_datetime: datetime.datetime):
        """
        Calculates the difference between the expected and actual datetime.

        Args:
            expected_datetime (datetime.datetime): The datetime to compare against.

        Returns:
            str: The difference between the two datetime in a human-readable format.
        """
        if not isinstance(self._actual_value, datetime.datetime):
            return ""

        difference = abs(self._actual_value - expected_datetime)
        return f"\nDatetime difference: {str(difference)}"

    def _numeric_difference(self, expected_value: Union[int, float]):
        """
        Calculates the difference between the expected and actual numeric value.

        Args:
            expected_value (Union[int, float]): The value to compare against.

        Returns:
            str: The difference between the two numeric values in a human-readable format.
        """
        if not isinstance(self._actual_value, (int, float)):
            return ""

        difference = abs(self._actual_value - expected_value)
        return f"\nNumeric difference: {str(difference)}"

    def _file_difference(self, expected_file_path):
        """
        Compare two text files and generate a git-like diff.

        Args:
            expected_file_path: The path of the expected file.

        Returns:
            A string detailing the differences.
        """
        # Checking if the actual value is a valid file path
        if not os.path.isfile(self._actual_value):
            return f"File does not exist: {self._actual_value}"

        # Checking if the expected value is a valid file path
        if not os.path.isfile(expected_file_path):
            return f"File does not exist: {expected_file_path}"

        # Checking file extensions
        _, actual_extension = os.path.splitext(self._actual_value)
        _, expected_extension = os.path.splitext(expected_file_path)

        if (
            actual_extension not in self.allowed_extensions_for_file_difference
            or expected_extension not in self.allowed_extensions_for_file_difference
        ):
            return f"File extension not supported for diff: {actual_extension} or {expected_extension}"

        # Reading files
        with open(self._actual_value, "r") as file:
            actual_content = file.readlines()

        with open(expected_file_path, "r") as file:
            expected_content = file.readlines()

        # Comparing files
        diff = difflib.unified_diff(actual_content, expected_content)

        # Filtering only lines with differences and joining them into a single string
        diff_lines = [
            line for line in diff if line.startswith("+") or line.startswith("-")
        ]
        diff_string = "".join(diff_lines)

        return f"\nFile difference:\n{diff_string}"
