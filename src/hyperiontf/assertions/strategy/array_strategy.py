from .default_strategy import DefaultStrategy
from hyperiontf.assertions.expectation_result import ExpectationResult
from .decorators import with_array_diff


class ArrayStrategy(DefaultStrategy):
    types = [list, set, tuple]

    @with_array_diff
    def to_be(self, expected_value) -> ExpectationResult:
        """
        Checks if the actual collection (list, set, tuple) is equal to the expected collection. This method
        extends the basic equality check from DefaultStrategy with the addition of a detailed
        array difference in case of a failed comparison, using the with_array_diff decorator.

        This enhanced comparison is useful for cases where understanding the specific differences
        between the actual and expected collections is important, especially in testing scenarios
        where detailed feedback is valuable.

        Args:
            expected_value (collection): The collection (list, set, tuple) to compare against.

        Returns:
            ExpectationResult: The result of the collection comparison, including a detailed difference
                               if the comparison fails.
        """
        return super().to_be(expected_value)

    def to_contain(self, expected_value) -> ExpectationResult:
        """
        Checks if the collection contains the expected value.

        Args:
            expected_value: The value expected to be found in the collection.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = expected_value in self.actual_value
        human_readable_description = f"Check if collection contains '{expected_value}'"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="to_contain",
            human_readable_description=human_readable_description,
        )

    def to_have_length(self, expected_length) -> ExpectationResult:
        """
        Checks if the collection has the specified length.

        Args:
            expected_length: The expected length of the collection.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = len(self.actual_value) == expected_length
        human_readable_description = f"Check if collection has length {expected_length}"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_length,
            method="to_have_length",
            human_readable_description=human_readable_description,
        )

    def to_be_empty(self) -> ExpectationResult:
        """
        Checks if the collection is empty.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = len(self.actual_value) == 0
        human_readable_description = "Check if collection is empty"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=None,
            method="to_be_empty",
            human_readable_description=human_readable_description,
        )

    def not_to_be_empty(self) -> ExpectationResult:
        """
        Checks if the collection is not empty.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = len(self.actual_value) > 0
        human_readable_description = "Check if collection is not empty"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=None,
            method="not_to_be_empty",
            human_readable_description=human_readable_description,
        )

    def to_contain_exactly(self, *expected_elements) -> ExpectationResult:
        """
        Checks if the collection contains exactly the specified elements, no more, no less.
        This is useful for asserting the exact contents of a collection, regardless of order.

        Args:
            expected_elements: The elements expected to be exactly present in the collection.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = set(self.actual_value) == set(expected_elements)
        human_readable_description = (
            "Check if collection contains exactly the specified elements"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_elements,
            method="to_contain_exactly",
            human_readable_description=human_readable_description,
        )

    def to_contain_any_of(self, *expected_elements) -> ExpectationResult:
        """
        Checks if the collection contains any of the specified elements.

        Args:
            expected_elements: Elements at least one of which is expected to be found in the collection.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = any(element in self.actual_value for element in expected_elements)
        human_readable_description = (
            "Check if collection contains any of the specified elements"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_elements,
            method="to_contain_any_of",
            human_readable_description=human_readable_description,
        )

    def not_to_contain(self, expected_value) -> ExpectationResult:
        """
        Checks if the collection does not contain the expected value.

        Args:
            expected_value: The value expected not to be found in the collection.

        Returns:
            ExpectationResult: The result of the check, indicating whether the expected value
                               is not present in the collection. Includes the actual collection,
                               the expected absent value, the result of the check (True or False),
                               the method name for reference, and a human-readable description
                               of the check performed.
        """
        result = expected_value not in self.actual_value
        human_readable_description = (
            f"Check if collection does not contain '{expected_value}'"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_value,
            method="not_to_contain",
            human_readable_description=human_readable_description,
        )

    def not_to_contain_any_of(self, *expected_elements) -> ExpectationResult:
        """
        Checks if the collection does not contain any of the specified elements.

        Args:
            expected_elements: Elements none of which are expected to be found in the collection.

        Returns:
            ExpectationResult: The result of the check, indicating whether none of the specified
                               elements are present in the collection. Includes the actual collection,
                               the elements expected to be absent, the result of the check (True or False),
                               the method name for reference, and a human-readable description
                               of the check performed.
        """
        result = not any(element in self.actual_value for element in expected_elements)
        human_readable_description = (
            "Check if collection does not contain any of the specified elements"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_elements,
            method="not_to_contain_any_of",
            human_readable_description=human_readable_description,
        )
