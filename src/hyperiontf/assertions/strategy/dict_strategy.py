from .default_strategy import DefaultStrategy
from hyperiontf.assertions.expectation_result import ExpectationResult
from .decorators import with_dict_diff

import jsonschema
import json


class DictStrategy(DefaultStrategy):
    types = [dict]

    @with_dict_diff
    def to_be(self, expected_value) -> ExpectationResult:
        """
        Checks if the actual dictionary is equal to the expected dictionary. This method
        leverages the with_dict_diff decorator to provide detailed feedback on the comparison
        when the assertion fails, highlighting missing keys, added keys, and mismatching values.

        Args:
            expected_value (dict): The dictionary to compare against the actual dictionary.

        Returns:
            ExpectationResult: The result of the dictionary comparison, including detailed
                               differences if the comparison fails.
        """
        # Assuming super().to_be performs a basic equality check and the decorator handles the diff.
        return super().to_be(expected_value)

    def to_contain_key(self, key) -> ExpectationResult:
        """
        Checks if the actual dictionary contains the specified key.

        Args:
            key: The key expected to be present in the dictionary.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = key in self.actual_value
        human_readable_description = f"Check if dictionary contains key '{key}'"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=key,
            method="to_contain_key",
            human_readable_description=human_readable_description,
        )

    def to_contain_keys(self, *keys) -> ExpectationResult:
        """
        Checks if the actual dictionary contains all the specified keys.

        Args:
            keys: The keys expected to be present in the dictionary.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = all(key in self.actual_value for key in keys)
        human_readable_description = f"Check if dictionary contains keys {keys}"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=keys,
            method="to_contain_keys",
            human_readable_description=human_readable_description,
        )

    def to_contain_value(self, value) -> ExpectationResult:
        """
        Checks if the actual dictionary contains the specified value.

        Args:
            value: The value expected to be present in the dictionary.

        Returns:
            ExpectationResult: The result of the check.
        """
        result = value in self.actual_value.values()
        human_readable_description = f"Check if dictionary contains value '{value}'"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=value,
            method="to_contain_value",
            human_readable_description=human_readable_description,
        )

    def not_to_contain_key(self, key) -> ExpectationResult:
        """
        Checks if the actual dictionary does not contain the specified key.

        Args:
            key: The key expected not to be present in the dictionary.

        Returns:
            ExpectationResult: The result of the check, indicating whether the specified key
                               is absent from the dictionary. Includes the actual dictionary,
                               the key checked for absence, the result of the check (True or False),
                               the method name for reference, and a human-readable description
                               of the check performed.
        """
        result = key not in self.actual_value
        human_readable_description = f"Check if dictionary does not contain key '{key}'"
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=key,
            method="not_to_contain_key",
            human_readable_description=human_readable_description,
        )

    def not_to_contain_keys(self, *keys) -> ExpectationResult:
        """
        Checks if the actual dictionary does not contain any of the specified keys.

        Args:
            keys: A sequence of keys expected not to be present in the dictionary.

        Returns:
            ExpectationResult: The result of the check, indicating whether all of the specified keys
                               are absent from the dictionary. Includes the actual dictionary,
                               the keys checked for absence, the result of the check (True or False),
                               the method name for reference, and a human-readable description
                               of the check performed.
        """
        result = not any(key in self.actual_value for key in keys)
        human_readable_description = (
            f"Check if dictionary does not contain any of the keys {keys}"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=keys,
            method="not_to_contain_keys",
            human_readable_description=human_readable_description,
        )

    def not_to_contain_value(self, value) -> ExpectationResult:
        """
        Checks if the actual dictionary does not contain the specified value.

        Args:
            value: The value expected not to be present in the dictionary.

        Returns:
            ExpectationResult: The result of the check, indicating whether the specified value
                               is absent from the dictionary. Includes the actual dictionary,
                               the value checked for absence, the result of the check (True or False),
                               the method name for reference, and a human-readable description
                               of the check performed.
        """
        result = value not in self.actual_value.values()
        human_readable_description = (
            f"Check if dictionary does not contain value '{value}'"
        )
        return ExpectationResult(
            result=result,
            actual_value=self.actual_value,
            expected_value=value,
            method="not_to_contain_value",
            human_readable_description=human_readable_description,
        )

    def to_match_schema(self, schema) -> ExpectationResult:
        """
        Validates the actual dictionary against the provided JSON Schema. The schema can be
        provided directly as a dictionary representing the JSON Schema or as a string path
        to a JSON Schema file.

        Args:
            schema (Union[dict, str]): The JSON Schema to validate against, either as a dictionary
                                       or a string path to a JSON Schema file.

        Returns:
            ExpectationResult: The result of the JSON Schema validation, including a human-readable
                               description of the action performed. If the validation fails, the 'diff'
                               property of the result will contain the validation error message.
        """
        if isinstance(schema, str):
            # Load the JSON Schema from file if a string is provided
            with open(schema, "r") as schema_file:
                schema = json.load(schema_file)

        message = "Validate dictionary against the JSON Schema."
        result = ExpectationResult(
            result=True,
            actual_value=self.actual_value,
            expected_value=schema,
            method="to_match_schema",
            human_readable_description=message,
        )

        try:
            jsonschema.validate(instance=self.actual_value, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            result.result = False
            result.diff = e.message

        return result
