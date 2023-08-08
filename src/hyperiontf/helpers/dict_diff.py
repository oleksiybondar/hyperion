def extra_fields_analysis(actual_fields, expected_fields) -> str:
    """
    Analyze and report extra fields present in either of the two sets of dictionary keys.

    Args:
    actual_fields (set): A set of keys from the actual dictionary.
    expected_fields (set): A set of keys from the expected dictionary.

    Returns:
    str: A message string listing extra fields found in either the actual or expected dictionaries.
    """
    extra_in_actual = actual_fields - expected_fields
    extra_in_expected = expected_fields - actual_fields
    message = ""

    if extra_in_actual:
        message += f"\nActual dictionary has extra fields: {extra_in_actual}"
    if extra_in_expected:
        message += f"\nExpected dictionary has extra fields: {extra_in_expected}"

    return message


def value_differences_analysis(actual, expected, common_fields) -> str:
    """
    Analyze and report differences in values for common fields between two dictionaries.

    Args:
    actual (dict): The actual dictionary.
    expected (dict): The expected dictionary.
    common_fields (set): A set of keys that are common to both dictionaries.

    Returns:
    str: A message string detailing discrepancies in values for common fields.
    """
    message = ""
    for field in common_fields:
        if actual[field] != expected[field]:
            message += f"\n'{field}' field: actual value {actual[field]} is not equal to expected value {expected[field]}"
    return message


def dict_diff(actual, expected) -> str:
    """
    Compare two dictionaries and compile a message detailing their differences.

    This function uses helper functions to identify extra fields and value discrepancies
    in common fields between the two dictionaries.

    Args:
    actual (dict): The actual dictionary to compare.
    expected (dict): The expected dictionary to compare against.

    Returns:
    str: A compiled message string describing all differences found between the dictionaries.
    """
    actual_fields = set(actual.keys())
    expected_fields = set(expected.keys())

    # Analyze extra fields
    extra_fields_message = extra_fields_analysis(actual_fields, expected_fields)

    # Analyze value differences in common fields
    common_fields = actual_fields.intersection(expected_fields)
    value_diff_message = value_differences_analysis(actual, expected, common_fields)

    # Combine messages
    return extra_fields_message + value_diff_message
