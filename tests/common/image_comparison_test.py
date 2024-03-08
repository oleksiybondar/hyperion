import pytest
from hyperiontf.executors.pytest import automatic_log_setup  # noqa: F401
from hyperiontf import verify, Image

# from hyperiontf.typing import FailedExpectationException

import os

current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, "..", "resources", "images")
images_abs_path = os.path.abspath(images_dir)

base_img = os.path.join(images_abs_path, "base.jpg")
modified_img = os.path.join(images_abs_path, "modified.jpg")

base = Image(base_img)
modified = Image(modified_img)

variants = [
    {"method": "to_be", "actual": base, "expected": base, "result": True, "args": []},
    {
        "method": "to_be",
        "actual": base,
        "expected": modified,
        "result": False,
        "args": [],
    },
    {
        "method": "to_be_similar",
        "actual": base,
        "expected": modified,
        "result": True,
        "args": [],
    },
    {
        "method": "to_be_similar",
        "actual": base,
        "expected": modified,
        "result": False,
        "args": [1],
    },
]


@pytest.mark.parametrize("test_case", variants)
@pytest.mark.expect
@pytest.mark.methods
@pytest.mark.visual
def test_basic_visual_testing_functionality(test_case):
    actual_value = test_case["actual"]
    expected_value = test_case["expected"]
    expected_result = test_case["result"]
    expect_object = verify(actual_value)
    method = getattr(expect_object, test_case["method"])
    arguments = test_case["args"]
    result = method(expected_value, *arguments)
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
