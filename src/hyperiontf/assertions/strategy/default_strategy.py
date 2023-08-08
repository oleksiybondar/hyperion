from hyperiontf.assertions.expectation_result import ExpectationResult
from datetime import date, time, datetime


class DefaultStrategy:
    """
    Base strategy class for handling various type-insensitive comparison methods.
    """

    def __init__(self, actual_value):
        """
        Initializes the DefaultStrategy with the actual value to be tested.

        Args:
            actual_value (Any): The actual value to be used in expectations.
        """
        self.actual_value = actual_value

    def is_none(self) -> ExpectationResult:
        """
        Checks if the actual value is None.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        result = self.actual_value is None
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=None,
            method="is_none",
        )

    def is_not_none(self) -> ExpectationResult:
        """
        Checks if the actual value is not None.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        result = self.actual_value is not None
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=None,
            method="is_not_none",
        )

    def is_a(self, cls) -> ExpectationResult:
        """
        Checks if the actual value is an instance of the specified class.

        Args:
            cls (Type): The class to check against.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        result = isinstance(self.actual_value, cls)
        human_readable_description = f"Check if value is an instance of {cls.__name__}"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=cls,
            method="is_a",
            human_readable_description=human_readable_description,
        )

    def is_not_a(self, cls) -> ExpectationResult:
        """
        Checks if the actual value is not an instance of the specified class.

        Args:
            cls (Type): The class to check against.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        result = not isinstance(self.actual_value, cls)
        human_readable_description = (
            f"Check if value is not an instance of {cls.__name__}"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=cls,
            method="is_not_a",
            human_readable_description=human_readable_description,
        )

    def is_type_of(self, cls) -> ExpectationResult:
        """
        Checks if the actual value's type is exactly the specified class.

        Args:
            cls (Type): The class to check against.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        result = type(self.actual_value) is cls
        human_readable_description = f"Check if value's type is exactly {cls.__name__}"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=cls,
            method="is_type_of",
            human_readable_description=human_readable_description,
        )

    def is_not_type_of(self, cls) -> ExpectationResult:
        """
        Checks if the actual value's type is not exactly the specified class.

        Args:
            cls (Type): The class to check against.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        result = type(self.actual_value) is not cls
        human_readable_description = (
            f"Check if value's type is not exactly {cls.__name__}"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=cls,
            method="is_not_type_of",
            human_readable_description=human_readable_description,
        )

    def is_string(self) -> ExpectationResult:
        """
        Checks if the actual value is a string.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_a(str)

    def is_int(self) -> ExpectationResult:
        """
        Checks if the actual value is an integer.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_a(int)

    def is_float(self) -> ExpectationResult:
        """
        Checks if the actual value is a floating point number.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_a(float)

    def is_bool(self) -> ExpectationResult:
        """
        Checks if the actual value is a boolean.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_a(bool)

    def is_date(self) -> ExpectationResult:
        """
        Checks if the actual value is a date object.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_a(date)

    def is_time(self) -> ExpectationResult:
        """
        Checks if the actual value is a time object.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_a(time)

    def is_datetime(self) -> ExpectationResult:
        """
        Checks if the actual value is a datetime object.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_a(datetime)

    def is_list(self) -> ExpectationResult:
        """
        Checks if the actual value is a list.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_a(list)

    def is_dict(self) -> ExpectationResult:
        """
        Checks if the actual value is a dictionary.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_a(dict)

    def to_be(self, expected_value) -> ExpectationResult:
        """
        Checks if the actual value is equal to the expected value.

        Args:
            expected_value: The value to compare against.

        Returns:
            ExpectationResult: The result of the equality check.
        """
        result = self.actual_value == expected_value
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="to_be",
        )

    def not_to_be(self, expected_value) -> ExpectationResult:
        """
        Checks if the actual value is not equal to the expected value.

        Args:
            expected_value: The value to compare against.

        Returns:
            ExpectationResult: The result of the inequality check.
        """
        result = self.actual_value != expected_value
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="not_to_be",
        )

    def is_not_string(self) -> ExpectationResult:
        """
        Checks if the actual value is not a string.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_not_a(str)

    def is_not_int(self) -> ExpectationResult:
        """
        Checks if the actual value is not an integer.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_not_a(int)

    def is_not_float(self) -> ExpectationResult:
        """
        Checks if the actual value is not a floating point number.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_not_a(float)

    def is_not_bool(self) -> ExpectationResult:
        """
        Checks if the actual value is not a boolean.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_not_a(bool)

    def is_not_date(self) -> ExpectationResult:
        """
        Checks if the actual value is not a date object.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_not_a(date)

    def is_not_time(self) -> ExpectationResult:
        """
        Checks if the actual value is not a time object.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_not_a(time)

    def is_not_datetime(self) -> ExpectationResult:
        """
        Checks if the actual value is not a datetime object.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_not_a(datetime)

    def is_not_list(self) -> ExpectationResult:
        """
        Checks if the actual value is not a list.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_not_a(list)

    def is_not_dict(self) -> ExpectationResult:
        """
        Checks if the actual value is not a dictionary.

        Returns:
            ExpectationResult: Result of the check, including details for logging and assertion.
        """
        return self.is_not_a(dict)
