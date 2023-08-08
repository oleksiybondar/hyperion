import pytest
from hyperiontf.executors.pytest import automatic_log_setup  # noqa: F401
from hyperiontf import expect, verify, Color
from hyperiontf.typing import FailedExpectationException

# Arrays for test cases
type_assertions_tests = [
    {
        "method": "to_be_approximately_equal",
        "actual": 1,
        "expected": "rgb(1,1,1)",
        "exception_message": "to_be_approximately_equal can be called for types Color, but got int.",
    },
    {
        "method": "not_to_be_multiple_of",
        "actual": "test",
        "expected": 3.0,
        "exception_message": "not_to_be_multiple_of can be called for types bool, float, int, but got str",
    },
    {
        "method": "to_contain",
        "actual": 100,
        "expected": "value",
        "exception_message": "to_contain can be called for types list, set, str, tuple, but got int.",
    },
    {
        "method": "to_start_with",
        "actual": False,
        "expected": "prefix",
        "exception_message": "to_start_with can be called for types str, but got bool.",
    },
    {
        "method": "to_contain_key",
        "actual": [1, 2, 3],
        "expected": "key",
        "exception_message": "to_contain_key can be called for types dict, but got list.",
    },
    {
        "method": "to_be_file",
        "actual": 123,
        "expected": None,
        "exception_message": "to_be_file can be called for types Dir, File, but got int.",
    },
]

assertions_tests = [
    {"actual_value": 42, "expected_value": 42, "result": True},
    {"actual_value": 42, "expected_value": 43, "result": False},
]

methods_operability_tests = [
    # Type-Independent Method with Positive Expectation
    {"method": "is_bool", "actual_value": True, "arguments": [], "result": True},
    # Type-Independent Method with Negative Expectation
    {"method": "is_bool", "actual_value": 10, "arguments": [], "result": False},
    # String Method
    {
        "method": "to_contain",
        "actual_value": "hello world",
        "arguments": ["world"],
        "result": True,
    },
    # Array Method
    {
        "method": "to_have_length",
        "actual_value": [1, 2, 3],
        "arguments": [3],
        "result": True,
    },
    # Numeric Method
    {
        "method": "to_be_greater_than",
        "actual_value": 5,
        "arguments": [3],
        "result": True,
    },
    # Method with Two or More Arguments
    {
        "method": "to_be_in_range",
        "actual_value": 5,
        "arguments": [1, 10],
        "result": True,
    },
    {"method": "to_be", "actual_value": 10, "arguments": [10], "result": True},
    {"method": "to_be", "actual_value": "test", "arguments": ["test"], "result": True},
    {
        "method": "to_be",
        "actual_value": Color.from_string("rgba(255,200,100, 1)"),
        "arguments": ["rgba(255,200,100, 1)"],
        "result": True,
    },
    {"method": "not_to_be", "actual_value": 10, "arguments": [5], "result": True},
    {"method": "to_be_less_than", "actual_value": 5, "arguments": [10], "result": True},
    {
        "method": "to_be_greater_than",
        "actual_value": 10,
        "arguments": [5],
        "result": True,
    },
    {
        "method": "to_contain",
        "actual_value": [1, 2, 3],
        "arguments": [2],
        "result": True,
    },
    {
        "method": "to_start_with",
        "actual_value": "hello",
        "arguments": ["he"],
        "result": True,
    },
    {
        "method": "to_end_with",
        "actual_value": "world",
        "arguments": ["ld"],
        "result": True,
    },
    {
        "method": "to_contain_key",
        "actual_value": {"key": "value"},
        "arguments": ["key"],
        "result": True,
    },
    {
        "method": "to_be_approximately_equal",
        "actual_value": Color.from_string("rgba(255,200,100, 1)"),
        "arguments": ["rgba(250,205,100, 1)"],
        "result": True,
    },
]

differences_tests = [
    {
        "actual_value": "hello",
        "expected_value": "hello",
        "with_diff": True,
        "diff": None,
    },
    {
        "actual_value": "hello",
        "expected_value": "world",
        "with_diff": True,
        "diff": "^^^l^",
    },
    {
        "actual_value": [1, 2, 3],
        "expected_value": [1, 2, 3],
        "with_diff": True,
        "diff": None,
    },
    {
        "actual_value": [1, 2, 3],
        "expected_value": [4, 5, 6],
        "with_diff": True,
        "diff": "[^, ^, ^]",
    },
    {
        "actual_value": {"key": "value"},
        "expected_value": {"key": "value"},
        "with_diff": True,
        "diff": None,
    },
    {
        "actual_value": {"key": "value"},
        "expected_value": {"key": "different"},
        "with_diff": True,
        "diff": "\n'key' "
        "field: "
        "actual "
        "value "
        "value is "
        "not equal "
        "to "
        "expected "
        "value "
        "different",
    },
]


@pytest.mark.parametrize("test_case", type_assertions_tests)
@pytest.mark.expect
@pytest.mark.type_assertions
def test_type_assertions(test_case):
    """
    Test methods decorated with type assertions to ensure they raise exceptions
    when called with incompatible types. This verifies the robustness of the
    type-checking mechanism.
    """
    actual_value = test_case["actual"]
    exception_message = test_case["exception_message"]
    expected_value = test_case["expected"]
    expect_object = expect(actual_value)
    method = getattr(expect_object, test_case["method"])
    with pytest.raises(TypeError, match=exception_message):
        method(expected_value)


@pytest.mark.parametrize("test_case", assertions_tests)
@pytest.mark.expect
@pytest.mark.assertions
def test_assertions(test_case):
    """
    Verify assertions raise exceptions when expectations fail and correctly return
    a result when expectations pass. This test ensures the assertion mechanism
    functions as intended for both passing and failing conditions.
    """
    actual_value = test_case["actual_value"]
    result = test_case["result"]
    expected_value = test_case["expected_value"]
    if not result:
        with pytest.raises(FailedExpectationException):
            expect(actual_value).to_be(expected_value)
    else:
        assert expect(actual_value).to_be(expected_value)


@pytest.mark.parametrize("test_case", methods_operability_tests)
@pytest.mark.expect
@pytest.mark.methods
def test_methods_operability(test_case):
    """
    Test the operability of `Expect` class methods by verifying their expected
    outcomes using `verify`. This ensures that methods perform as intended and
    the `ExpectationResult` fields are correctly populated.
    """
    actual_value = test_case["actual_value"]
    expected_result = test_case["result"]
    expect_object = verify(actual_value)
    method = getattr(expect_object, test_case["method"])
    arguments = test_case["arguments"]
    result = method(*arguments)
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


@pytest.mark.parametrize("test_case", differences_tests)
@pytest.mark.expect
@pytest.mark.differences
def test_differences(test_case):
    """
    Test the `with_diff` helper to ensure `to_be` method can generate and return
    a difference string for strings, lists, and dictionaries upon failure. This
    verifies the utility of providing detailed difference information for failed
    assertions.
    """
    actual_value = test_case["actual_value"]
    expected_value = test_case["expected_value"]
    diff = test_case["diff"]
    result = verify(actual_value).to_be(expected_value)
    assert result.diff == diff
