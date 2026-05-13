import json

import jsonschema

from hyperiontf.assertions.expectation_result import ExpectationResult

from .default_strategy import DefaultStrategy


class JSONSchemedStrategy(DefaultStrategy):
    types = [dict, list, set, tuple]

    def to_match_schema(self, schema) -> ExpectationResult:
        """
        Validates the actual value against the provided JSON Schema. The schema can be
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
            with open(schema, "r") as schema_file:
                schema = json.load(schema_file)

        message = "Validate value against the JSON Schema."
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
