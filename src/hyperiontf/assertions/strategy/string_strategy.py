from .default_strategy import DefaultStrategy
from hyperiontf.assertions.expectation_result import ExpectationResult
import re
from .decorators import with_string_diff


class StringStrategy(DefaultStrategy):
    types = [str]

    @with_string_diff
    def to_be(self, expected_value) -> ExpectationResult:
        """
        Checks if the actual string value is equal to the expected string value. This method
        extends the basic equality check from DefaultStrategy with the addition of a detailed
        string difference in case of a failed comparison, using the with_string_diff decorator.

        This enhanced comparison is useful for cases where understanding the specific differences
        between the actual and expected strings is important, especially in testing scenarios
        where detailed feedback is valuable.

        Args:
            expected_value (str): The string value to compare against.

        Returns:
            ExpectationResult: The result of the string comparison, including a detailed difference
                               if the comparison fails.
        """
        return super().to_be(expected_value)

    @with_string_diff
    def to_start_with(self, prefix) -> ExpectationResult:
        """
        Checks if the actual string value starts with the specified prefix. This method is useful
        for validating the beginning of a string against a known substring.

        The method is decorated with `with_string_diff` to provide a detailed string difference
        in case the actual string does not start with the expected prefix, enhancing the
        debuggability of test failures.

        Args:
            prefix (str): The substring expected at the beginning of the actual value.

        Returns:
            ExpectationResult: The result of the check, including a detailed difference if the
                               actual string does not start with the specified prefix.
        """
        result = self.actual_value.startswith(prefix)
        human_readable_description = f"Check if string starts with '{prefix}'"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=prefix,
            method="to_start_with",
            human_readable_description=human_readable_description,
        )

    @with_string_diff
    def to_end_with(self, suffix) -> ExpectationResult:
        """
        Checks if the actual string value ends with the specified suffix. This method is used
        for validating the end of a string against a known substring.

        Similar to 'starts_with', this method is decorated with `with_string_diff` to provide
        a detailed string difference in case the actual string does not end with the expected
        suffix. This feature is particularly useful for debugging failures in string comparison
        tests where the ending of the string is of interest.

        Args:
            suffix (str): The substring expected at the end of the actual value.

        Returns:
            ExpectationResult: The result of the check, including a detailed difference if the
                               actual string does not end with the specified suffix.
        """
        result = self.actual_value.endswith(suffix)
        human_readable_description = f"Check if string ends with '{suffix}'"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=suffix,
            method="to_end_with",
            human_readable_description=human_readable_description,
        )

    @with_string_diff
    def to_contain(self, substring) -> ExpectationResult:
        """
        Checks if the actual string value contains the specified substring. This method is useful
        for verifying that a certain piece of text is present within the actual string value.

        This method is enhanced with `with_string_diff` to provide a detailed string difference
        in case the actual string does not contain the expected substring.

        Args:
            substring (str): The substring to check for within the actual value.

        Returns:
            ExpectationResult: The result of the check, including a detailed difference if the
                               actual string does not contain the specified substring.
        """
        result = substring in self.actual_value
        human_readable_description = f"Check if string contains '{substring}'"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=substring,
            method="to_contain",
            human_readable_description=human_readable_description,
        )

    def to_match(self, pattern) -> ExpectationResult:
        """
        Checks if any part of the actual string value matches the specified regular expression pattern.
        This method is versatile for various types of pattern matching within the entire string,
        making it a powerful tool for complex text validation.

        Args:
            pattern (str): The regular expression pattern to search for within the actual string value.

        Returns:
            ExpectationResult: The result of the regex search check. The result is True if any part of
                               the actual string matches the pattern, and False otherwise.
        """
        regex = re.compile(pattern)
        result = bool(regex.search(self.actual_value))
        human_readable_description = (
            f"Check if string matches (anywhere) the regex pattern '{pattern}'"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=pattern,
            method="to_match",
            human_readable_description=human_readable_description,
        )

    def to_be_empty(self) -> ExpectationResult:
        """
        Checks if the actual string value is empty after stripping whitespace. This considers strings
        that only contain whitespace characters (spaces, tabs, newlines, etc.) as empty.

        This method is particularly useful for validating that a string is either completely empty or
        contains only whitespace, which can be important in user input validation, data processing,
        or checking API responses where whitespace should not be considered meaningful content.

        Returns:
            ExpectationResult: The result of the check, indicating whether the actual string is empty
                               or contains only whitespace.
        """
        result = len(self.actual_value.strip()) == 0
        human_readable_description = (
            "Check if string is empty or contains only whitespace"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value="",
            method="to_be_empty",
            human_readable_description=human_readable_description,
        )

    def not_to_start_with(self, prefix) -> ExpectationResult:
        """
        Checks if the actual string value does not start with the specified prefix.
        """
        result = not self.actual_value.startswith(prefix)
        human_readable_description = f"Check if string does not start with '{prefix}'"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=prefix,
            method="not_to_start_with",
            human_readable_description=human_readable_description,
        )

    def not_to_end_with(self, suffix) -> ExpectationResult:
        """
        Checks if the actual string value does not end with the specified suffix.
        """
        result = not self.actual_value.endswith(suffix)
        human_readable_description = f"Check if string does not end with '{suffix}'"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=suffix,
            method="not_to_end_with",
            human_readable_description=human_readable_description,
        )

    def not_to_contain(self, substring) -> ExpectationResult:
        """
        Checks if the actual string value does not contain the specified substring.
        """
        result = substring not in self.actual_value
        human_readable_description = f"Check if string does not contain '{substring}'"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=substring,
            method="not_to_contain",
            human_readable_description=human_readable_description,
        )

    def not_to_match(self, pattern) -> ExpectationResult:
        """
        Checks if any part of the actual string value does not match the specified regular expression pattern.
        """
        regex = re.compile(pattern)
        result = not bool(regex.search(self.actual_value))
        human_readable_description = (
            f"Check if string does not match (anywhere) the regex pattern '{pattern}'"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=pattern,
            method="not_to_match",
            human_readable_description=human_readable_description,
        )

    def not_to_be_empty(self) -> ExpectationResult:
        """
        Checks if the actual string value is not empty or contains more than just whitespace.
        """
        result = len(self.actual_value.strip()) != 0
        human_readable_description = (
            "Check if string is not empty or contains more than just whitespace"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value="",
            method="not_to_be_empty",
            human_readable_description=human_readable_description,
        )

    def to_have_length(self, expected_length) -> ExpectationResult:
        """
        Checks if the actual string value has the specified length. This method is useful
        for validating the exact length of a string, ensuring that a string meets specific size
        criteria, which can be important in contexts like input validation, data formatting,
        or protocol compliance.

        Args:
            expected_length (int): The expected length of the string.

        Returns:
            ExpectationResult: The result of the check, indicating whether the actual string has the
                               specified length. Includes the actual length, the expected length, the result
                               of the check (True or False), the method name for reference, and a human-readable
                               description of the check performed.
        """
        result = len(self.actual_value) == expected_length
        human_readable_description = f"Check if string has length {expected_length}"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=expected_length,
            method="to_have_length",
            human_readable_description=human_readable_description,
        )

    def to_contain_in_order(self, *substrings) -> ExpectationResult:
        """
        Checks if the actual string contains all specified substrings in the given order.
        The substrings do not need to be adjacent but must appear in sequence.

        Args:
            substrings (tuple of str): The substrings to check for in the actual string value.

        Returns:
            ExpectationResult: The result of the check, indicating whether the actual string contains
                               the specified substrings in order. Includes the actual string, the substrings,
                               the result of the check (True or False), the method name for reference, and
                               a human-readable description of the check performed.
        """
        current_search_position = 0
        result = True
        for substring in substrings:
            # Find each substring in the string starting from the last match's end
            found_position = self.actual_value.find(substring, current_search_position)
            if found_position == -1:
                result = False
                break
            else:
                # Move the search position ahead for the next iteration
                current_search_position = found_position + len(substring)

        human_readable_description = f"Check if string contains these substrings in order: {', '.join(substrings)}"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=substrings,
            method="to_contain_in_order",
            human_readable_description=human_readable_description,
        )
