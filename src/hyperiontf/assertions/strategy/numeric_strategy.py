from .default_strategy import DefaultStrategy
from hyperiontf.assertions.expectation_result import ExpectationResult


class NumericStrategy(DefaultStrategy):
    types = [bool, int, float]

    def to_be_odd(self) -> ExpectationResult:
        """
        Checks if the actual value is an odd number.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = self.actual_value % 2 != 0
        human_readable_description = "Check if value is an odd number"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=None,
            method="to_be_odd",
            human_readable_description=human_readable_description,
        )

    def to_be_even(self) -> ExpectationResult:
        """
        Checks if the actual value is an even number.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = self.actual_value % 2 == 0
        human_readable_description = "Check if value is an even number"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=None,
            method="to_be_even",
            human_readable_description=human_readable_description,
        )

    def to_be_positive(self) -> ExpectationResult:
        """
        Checks if the actual value is positive.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = self.actual_value > 0
        human_readable_description = "Check if value is positive"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=None,
            method="to_be_positive",
            human_readable_description=human_readable_description,
        )

    def to_be_negative(self) -> ExpectationResult:
        """
        Checks if the actual value is negative.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = self.actual_value < 0
        human_readable_description = "Check if value is negative"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=None,
            method="to_be_negative",
            human_readable_description=human_readable_description,
        )

    def to_be_in_between(self, lower_bound, upper_bound) -> ExpectationResult:
        """
        Checks if the actual value is between the specified lower and upper bounds.

        Args:
            lower_bound: The lower bound of the range.
            upper_bound: The upper bound of the range.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = lower_bound < self.actual_value < upper_bound
        human_readable_description = (
            f"Check if value is between {lower_bound} and {upper_bound}"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=(lower_bound, upper_bound),
            method="to_be_in_between",
            human_readable_description=human_readable_description,
        )

    def not_to_be_in_between(self, lower_bound, upper_bound) -> ExpectationResult:
        """
        Checks if the actual value is not between the specified lower and upper bounds.

        Args:
            lower_bound: The lower bound of the range.
            upper_bound: The upper bound of the range.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = not (lower_bound < self.actual_value < upper_bound)
        human_readable_description = (
            f"Check if value is not between {lower_bound} and {upper_bound}"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=(lower_bound, upper_bound),
            method="not_to_be_in_between",
            human_readable_description=human_readable_description,
        )

    def to_be_in_range(
        self, lower_bound: float, upper_bound: float
    ) -> ExpectationResult:
        """
        Asserts that the actual numeric value is within a specified range, inclusive of the boundary values.
        This method ensures that the value lies between or equals the lower and upper bounds, which is crucial
        for validations requiring values to adhere to a defined inclusive numerical range.

        Args:
            lower_bound (float): The inclusive lower limit of the range.
            upper_bound (float): The inclusive upper limit of the range.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual numeric
                               value is within the specified inclusive range. The result includes the actual value,
                               the specified range, and whether the check passed or failed.

        Note:
            This method enhances numeric validations by allowing boundary values to be considered valid, catering to
            scenarios where inclusivity is essential for the operational or validation criteria being applied.
        """
        result = lower_bound <= self.actual_value <= upper_bound
        human_readable_description = (
            f"Check if value is in range [{lower_bound}, {upper_bound}]"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=(lower_bound, upper_bound),
            method="to_be_in_range",
            human_readable_description=human_readable_description,
        )

    def not_to_be_in_range(
        self, lower_bound: float, upper_bound: float
    ) -> ExpectationResult:
        """
        Asserts that the actual numeric value does not lie within a specified range, inclusive of the boundary values.
        This method is vital for scenarios where the numeric value must fall outside the specified limits, crucial for
        exclusions where inclusivity extends to the boundary values themselves.

        Args:
            lower_bound (float): The inclusive lower limit of the range from which the value must be excluded.
            upper_bound (float): The inclusive upper limit of the range from which the value must be excluded.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual numeric
                               value is outside the specified inclusive range. It details the actual value, the specified
                               range, and whether the check passed or failed.

        Note:
            Utilizing this method ensures that numeric values are appropriately excluded from defined inclusive ranges,
            supporting precise control over acceptable value criteria and enhancing validation specificity.
        """
        result = not (lower_bound <= self.actual_value <= upper_bound)
        human_readable_description = (
            f"Check if value is not in range [{lower_bound}, {upper_bound}]"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=(lower_bound, upper_bound),
            method="not_to_be_in_range",
            human_readable_description=human_readable_description,
        )

    def to_be_close_to(self, expected_value, tolerance) -> ExpectationResult:
        """
        Checks if the actual value is approximately equal to the expected value within a certain tolerance.
        This method is particularly useful for floating-point comparisons where exact equality is not
        practical due to the nature of floating-point arithmetic.

        Args:
            expected_value: The value to which the actual value is compared.
            tolerance: The maximum difference between the actual and expected values for which they are
                       considered approximately equal.

        Returns:
            ExpectationResult: The result of the check, indicating if the actual value is close to the expected value.
        """
        result = abs(self.actual_value - expected_value) <= tolerance
        human_readable_description = f"Check if value is close to {expected_value} within a tolerance of {tolerance}"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="to_be_close_to",
            human_readable_description=human_readable_description,
        )

    def to_be_multiple_of(self, multiplier) -> ExpectationResult:
        """
        Checks if the actual value is a multiple of another number.

        Args:
            multiplier: The number to check if the actual value is a multiple of.

        Returns:
            ExpectationResult: The result of the check, indicating if the actual value is a multiple of the given number.
        """
        result = self.actual_value % multiplier == 0
        human_readable_description = f"Check if value is a multiple of {multiplier}"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=multiplier,
            method="to_be_multiple_of",
            human_readable_description=human_readable_description,
        )

    def to_be_true(self) -> ExpectationResult:
        """
        Checks if the actual value is True or 1. In contexts where this method is used,
        only True or 1 are considered as valid representations of truth.

        Returns:
            ExpectationResult: The result of the check, indicating if the actual value is True or 1.
        """
        result = self.actual_value is True or self.actual_value == 1
        human_readable_description = "Check if value is True or 1"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=True,
            method="to_be_true",
            human_readable_description=human_readable_description,
        )

    def to_be_false(self) -> ExpectationResult:
        """
        Checks if the actual value is False or 0. In contexts where this method is used,
        only False or 0 are considered as valid representations of falsehood.

        Returns:
            ExpectationResult: The result of the check, indicating if the actual value is False or 0.
        """
        result = self.actual_value is False or self.actual_value == 0
        human_readable_description = "Check if value is False or 0"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=False,
            method="to_be_false",
            human_readable_description=human_readable_description,
        )

    def to_be_zero(self) -> ExpectationResult:
        """
        Checks if the actual numeric value is zero. This method is useful for validating
        scenarios where the expected outcome is explicitly zero, such as in calculations
        or comparisons where zero has a specific significance.

        Returns:
            ExpectationResult: The result of the check, indicating if the actual value is zero.
        """
        result = self.actual_value == 0
        human_readable_description = "Check if numeric value is zero"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=0,
            method="to_be_zero",
            human_readable_description=human_readable_description,
        )

    def not_to_be_odd(self) -> ExpectationResult:
        """
        Checks if the actual value is not an odd number.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = self.actual_value % 2 == 0
        human_readable_description = "Check if value is not an odd number"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=None,
            method="not_to_be_odd",
            human_readable_description=human_readable_description,
        )

    def not_to_be_even(self) -> ExpectationResult:
        """
        Checks if the actual value is not an even number.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = self.actual_value % 2 != 0
        human_readable_description = "Check if value is not an even number"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=None,
            method="not_to_be_even",
            human_readable_description=human_readable_description,
        )

    def not_to_be_positive(self) -> ExpectationResult:
        """
        Checks if the actual value is not positive.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = self.actual_value <= 0
        human_readable_description = "Check if value is not positive"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=None,
            method="not_to_be_positive",
            human_readable_description=human_readable_description,
        )

    def not_to_be_negative(self) -> ExpectationResult:
        """
        Checks if the actual value is not negative.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = self.actual_value >= 0
        human_readable_description = "Check if value is not negative"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=None,
            method="not_to_be_negative",
            human_readable_description=human_readable_description,
        )

    def not_to_be_close_to(self, expected_value, tolerance) -> ExpectationResult:
        """
        Checks if the actual value is not approximately equal to the expected value within a certain tolerance.

        Args:
            expected_value: The value to which the actual value is compared.
            tolerance: The maximum difference between the actual and expected values for which they are
                       considered not approximately equal.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = abs(self.actual_value - expected_value) > tolerance
        human_readable_description = f"Check if value is not close to {expected_value} within a tolerance of {tolerance}"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="not_to_be_close_to",
            human_readable_description=human_readable_description,
        )

    def not_to_be_multiple_of(self, multiplier) -> ExpectationResult:
        """
        Checks if the actual value is not a multiple of another number.

        Args:
            multiplier: The number to check if the actual value is not a multiple of.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = self.actual_value % multiplier != 0
        human_readable_description = f"Check if value is not a multiple of {multiplier}"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=multiplier,
            method="not_to_be_multiple_of",
            human_readable_description=human_readable_description,
        )

    def not_to_be_zero(self) -> ExpectationResult:
        """
        Checks if the actual numeric value is not zero.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = self.actual_value != 0
        human_readable_description = "Check if numeric value is not zero"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=0,
            method="not_to_be_zero",
            human_readable_description=human_readable_description,
        )

    def to_be_greater_than(self, expected_value) -> ExpectationResult:
        """
        Checks if the actual value is greater than the expected value.

        Args:
            expected_value: The value to compare the actual value against.

        Returns:
            ExpectationResult: The result of the check, indicating if the actual value is greater than
                               the expected value. It includes the actual value, the expected value,
                               the result of the check (True or False), the method name for reference,
                               and a human-readable description of the check performed.
        """
        result = self.actual_value > expected_value
        human_readable_description = f"Check if value is greater than {expected_value}"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="to_be_greater_than",
            human_readable_description=human_readable_description,
        )

    def to_be_less_than(self, expected_value) -> ExpectationResult:
        """
        Checks if the actual value is less than the expected value.

        Args:
            expected_value: The value to compare the actual value against.

        Returns:
            ExpectationResult: The result of the check, indicating if the actual value is less than
                               the expected value. Includes detailed check information.
        """
        result = self.actual_value < expected_value
        human_readable_description = f"Check if value is less than {expected_value}"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="to_be_less_than",
            human_readable_description=human_readable_description,
        )

    def to_be_greater_than_or_equal_to(self, expected_value) -> ExpectationResult:
        """
        Checks if the actual value is greater than or equal to the expected value.

        Args:
            expected_value: The value to compare the actual value against.

        Returns:
            ExpectationResult: The result of the check, indicating if the actual value is greater than
                               or equal to the expected value. Includes detailed check information.
        """
        result = self.actual_value >= expected_value
        human_readable_description = (
            f"Check if value is greater than or equal to {expected_value}"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="to_be_greater_than_or_equal_to",
            human_readable_description=human_readable_description,
        )

    def to_be_less_than_or_equal_to(self, expected_value) -> ExpectationResult:
        """
        Checks if the actual value is less than or equal to the expected value.

        Args:
            expected_value: The value to compare the actual value against.

        Returns:
            ExpectationResult: The result of the check, indicating if the actual value is less than
                               or equal to the expected value. Includes detailed check information.
        """
        result = self.actual_value <= expected_value
        human_readable_description = (
            f"Check if value is less than or equal to {expected_value}"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="to_be_less_than_or_equal_to",
            human_readable_description=human_readable_description,
        )

    def to_be_divisible_by(self, expected_value) -> ExpectationResult:
        """
        Checks if the actual value is divisible by the expected value.

        Args:
            expected_value: The value to check divisibility against.

        Returns:
            ExpectationResult: The result of the check, indicating if the actual value is divisible by
                               the expected value. Includes detailed check information.
        """
        result = self.actual_value % expected_value == 0
        human_readable_description = f"Check if value is divisible by {expected_value}"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="to_be_divisible_by",
            human_readable_description=human_readable_description,
        )
