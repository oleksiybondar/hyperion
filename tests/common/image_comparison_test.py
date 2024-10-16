import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401
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
    {
        "method": "to_match_in_specified_regions",
        "actual": base,
        "expected": modified,
        "result": False,
        "args": [
            [
                {"x": 15, "y": 195, "width": 65, "height": 65},
            ],  # include regions
            10,  # mismatch threshold, there are still minor discrepancies due to antialiasing
        ],
    },
    {
        "method": "to_match_excluding_regions",
        "actual": base,
        "expected": modified,
        "result": True,
        "args": [
            [
                {"x": 15, "y": 95, "width": 160, "height": 320},
                {"x": 185, "y": 50, "width": 135, "height": 390},
                {"x": 325, "y": 93, "width": 130, "height": 310},
            ],  # exclude regions
            0.5,
            # mismatch threshold, there are still minor discrepancies due to antialiasing withing rest of the picture
        ],
    },
    {
        "method": "to_be_similar",
        "actual": base,
        "expected": modified,
        "result": True,
        "args": [
            10,  # mismatch threshold
            [
                {"x": 15, "y": 195, "width": 65, "height": 65},
                {"x": 185, "y": 50, "width": 125, "height": 125},
                {"x": 325, "y": 178, "width": 110, "height": 110},
            ],  # include regions
            [
                {"x": 43, "y": 203, "width": 10, "height": 50},
                {"x": 212, "y": 98, "width": 43, "height": 30},
            ],  # exclude regions
        ],
    },
]


@pytest.mark.parametrize("test_case", variants)
@pytest.mark.expect
@pytest.mark.Visual
def test_basic_visual_testing_functionality(test_case):
    actual_value = test_case["actual"]
    expected_value = test_case["expected"]
    expected_result = test_case["result"]
    expect_object = verify(actual_value)
    method = getattr(expect_object, test_case["method"])
    arguments = test_case["args"]
    result = method(expected_value, *arguments)
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
