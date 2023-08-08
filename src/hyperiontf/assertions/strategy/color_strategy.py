from .default_strategy import DefaultStrategy
from hyperiontf.assertions.expectation_result import ExpectationResult

from hyperiontf.ui.color import Color


def convert_str_to_color_for_expected(method):
    """
    Decorator that converts the expected value from a string to a Color object if necessary.

    This decorator is designed to be used with methods of the ColourStrategy class that take an expected
    color value as an argument. If the expected value is provided as a string representation of a color,
    this decorator converts it into a Color object by calling the Color.from_string method before
    passing it to the actual method. This allows the ColourStrategy methods to seamlessly handle
    color comparisons whether the expected color is provided as a Color object or as a string.

    The conversion is applied only to the expected value argument, and it assumes that the actual
    value is already a Color object, as part of the ColourStrategy's operation.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapper function that includes the string-to-Color conversion logic.
    """

    def wrapper(self, expected_value, *args, **kwargs):
        if isinstance(expected_value, str):
            expected_value = Color.from_string(expected_value)
        return method(self, expected_value, *args, **kwargs)

    return wrapper


class ColorStrategy(DefaultStrategy):
    types = [Color]

    @convert_str_to_color_for_expected
    def to_be(self, expected_value) -> ExpectationResult:
        """
        Checks if the actual Color object is equal to the expected Color object or color string.

        Args:
            expected_value (Color or str): The expected Color object or color string.

        Returns:
            ExpectationResult: The result of the color comparison.
        """
        return super().to_be(expected_value)

    @convert_str_to_color_for_expected
    def not_to_be(self, expected_value) -> ExpectationResult:
        """
        Checks if the actual Color object is not equal to the expected Color object or color string.

        Args:
            expected_value (Color or str): The expected Color object or color string.

        Returns:
            ExpectationResult: The result of the inverse color comparison.
        """
        return super().not_to_be(expected_value)

    @convert_str_to_color_for_expected
    def to_be_less_than(self, expected_value) -> ExpectationResult:
        """
        Checks if the grayscale value of the actual Color object is less than that of the expected Color object or color string.

        Args:
            expected_value (Color or str): The expected Color object or color string.

        Returns:
            ExpectationResult: The result of the comparison.
        """
        result = self.actual_value < expected_value
        message = (
            "Expecting actual color to be less in grayscale value than expected color"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="to_be_less_than",
            human_readable_description=message,
        )

    @convert_str_to_color_for_expected
    def to_be_greater_than(self, expected_value) -> ExpectationResult:
        """
        Checks if the grayscale value of the actual Color object is greater than that of the expected Color object or color string.

        Args:
            expected_value (Color or str): The expected Color object or color string to compare against.

        Returns:
            ExpectationResult: The result of the comparison.
        """
        result = self.actual_value > expected_value
        message = "Expecting actual color to have a greater grayscale value than the expected color"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="to_be_greater_than",
            human_readable_description=message,
        )

    @convert_str_to_color_for_expected
    def to_be_less_than_or_equal_to(self, expected_value) -> ExpectationResult:
        """
        Checks if the grayscale value of the actual Color object is less than or equal to that of the expected Color object or color string.

        Args:
            expected_value (Color or str): The expected Color object or color string to compare against.

        Returns:
            ExpectationResult: The result of the comparison.
        """
        result = self.actual_value <= expected_value
        message = "Expecting actual color to have a grayscale value less than or equal to the expected color"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="to_be_less_than_or_equal_to",
            human_readable_description=message,
        )

    @convert_str_to_color_for_expected
    def to_be_greater_than_or_equal_to(self, expected_value) -> ExpectationResult:
        """
        Checks if the grayscale value of the actual Color object is greater than or equal to that of the expected Color object or color string.

        Args:
            expected_value (Color or str): The expected Color object or color string to compare against.

        Returns:
            ExpectationResult: The result of the comparison.
        """
        result = self.actual_value >= expected_value
        message = "Expecting actual color to have a grayscale value greater than or equal to the expected color"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="to_be_greater_than_or_equal_to",
            human_readable_description=message,
        )

    @convert_str_to_color_for_expected
    def to_be_approximately_equal(
        self, expected_value, percentage_threshold=5, alpha_threshold=0.1
    ) -> ExpectationResult:
        """
        Checks if the actual Color object is approximately equal to another Color object,
        within specified thresholds for grayscale and alpha components.

        Args:
            expected_value (Color): The Color object to compare against.
            percentage_threshold (int): Grayscale percentage difference threshold.
            alpha_threshold (float): Alpha component difference threshold.

        Returns:
            ExpectationResult: The result of the approximate equality check.
        """
        result = self.actual_value.approx_eq(
            expected_value, percentage_threshold, alpha_threshold
        )
        message = "Expecting color to be approximately equal to another color"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="to_approx_eq",
            human_readable_description=message,
        )
