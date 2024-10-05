from typing import Optional, Union
from hyperiontf.image_processing.image import Image
from hyperiontf.assertions.image_expectation_result import ImageExpectationResult
from hyperiontf.logging import Logger
from hyperiontf.typing import VisualModeType, VisualMode
from .prepare_expect_object import prepare_expect_object


def _handle_mode(
    page_object, expected_value: Union[Image, str], mode: VisualModeType, logger: Logger
) -> Optional[Image]:
    """
    Handles the operation mode for visual comparison or update based on the provided mode argument.

    :param page_object: The object representing the current web page context.
    :param expected_value: The expected image or path to the expected image.
    :param mode: The mode of operation (compare or update).
    :param logger: Logger instance for logging purposes.
    :return: The screenshot image taken from the page object if in compare mode, otherwise None.
    """
    if isinstance(expected_value, Image):
        path = expected_value.path
    else:
        path = expected_value

    actual_image = page_object.make_screenshot(path)

    if mode == VisualMode.COMPARE:
        return actual_image

    logger.info(
        f"[{page_object.__full_name__}] Visual testing: collect mode --> Updating base image: {path}"
    )
    actual_image.write()
    return None


def verify_visual_match(
    page_object,
    expected_value: Union[Image, str],
    mismatch_threshold: float,
    compare_regions: Optional[list],
    exclude_regions: Optional[list],
    mode: VisualModeType,
    logger: Logger,
) -> ImageExpectationResult:
    """
    Verifies if the actual web page's visual appearance matches the expected image within the specified mismatch threshold.

    :param page_object: The object representing the current web page context.
    :param expected_value: The expected image or path to the expected image for comparison.
    :param mismatch_threshold: The allowable percentage difference between the images.
    :param compare_regions: Specific regions within the image to compare.
    :param exclude_regions: Regions within the image to exclude from the comparison.
    :param mode: The mode of operation (compare or update).
    :param logger: Logger instance for logging purposes.
    :return: An ImageExpectationResult indicating the outcome of the verification.
    """
    actual_image = _handle_mode(page_object, expected_value, mode, logger)
    if actual_image is None:
        return ImageExpectationResult(
            True,
            expected_value,
            expected_value,
            "verify_visual_match",
            False,
            logger,
            page_object.__full_name__,
        )

    expect_object = prepare_expect_object(
        page_object, actual_image, False, "Verifying visual match.", logger
    )
    return expect_object.to_be_similar(
        expected_value, mismatch_threshold, compare_regions, exclude_regions
    )


def assert_visual_match(
    page_object,
    expected_value: Union[Image, str],
    mismatch_threshold: float,
    compare_regions: Optional[list],
    exclude_regions: Optional[list],
    mode: VisualModeType,
    logger: Logger,
) -> ImageExpectationResult:
    """
    Asserts that the actual web page's visual appearance matches the expected image within a specified mismatch threshold.

    :param page_object: The object representing the current web page context.
    :param expected_value: The expected image or path to the expected image for comparison.
    :param mismatch_threshold: The allowable percentage difference between the images.
    :param compare_regions: Specific regions within the image to compare.
    :param exclude_regions: Regions within the image to exclude from the comparison.
    :param mode: The mode of operation (compare or update).
    :param logger: Logger instance for logging purposes.
    :return: An ImageExpectationResult indicating the outcome of the assertion.
    """
    actual_image = _handle_mode(page_object, expected_value, mode, logger)
    if actual_image is None:
        return ImageExpectationResult(
            True,
            expected_value,
            expected_value,
            "assert_visual_match",
            True,
            logger,
            page_object.__full_name__,
        )

    expect_object = prepare_expect_object(
        page_object, actual_image, True, "Asserting visual match.", logger
    )
    return expect_object.to_be_similar(
        expected_value, mismatch_threshold, compare_regions, exclude_regions
    )


def verify_visual_match_in_regions(
    page_object,
    expected_value: Union[Image, str],
    compare_regions: Optional[list],
    mismatch_threshold: float,
    mode: VisualModeType,
    logger: Logger,
):
    """
    Verifies the visual match for specified regions within the web page against the expected image.

    :param page_object: The object representing the current web page context.
    :param expected_value: The expected image or path to the expected image for comparison.
    :param compare_regions: Specific regions within the image to compare.
    :param mismatch_threshold: The allowable percentage difference within the specified regions.
    :param mode: The mode of operation (compare or update).
    :param logger: Logger instance for logging purposes.
    """
    actual_image = _handle_mode(page_object, expected_value, mode, logger)
    if actual_image is None:
        return ImageExpectationResult(
            True,
            expected_value,
            expected_value,
            "verify_visual_match_in_regions",
            False,
            logger,
            page_object.__full_name__,
        )

    expect_object = prepare_expect_object(
        page_object, actual_image, False, "Verifying partial visual match.", logger
    )
    return expect_object.to_match_in_specified_regions(
        expected_value, compare_regions, mismatch_threshold
    )


def assert_visual_match_in_regions(
    page_object,
    expected_value: Union[Image, str],
    compare_regions: Optional[list],
    mismatch_threshold: float,
    mode: VisualModeType,
    logger: Logger,
):
    """
    Asserts the visual match for specified regions within the web page against the expected image.

    :param page_object: The object representing the current web page context.
    :param expected_value: The expected image or path to the expected image for comparison.
    :param compare_regions: Specific regions within the image to compare.
    :param mismatch_threshold: The allowable percentage difference within the specified regions.
    :param mode: The mode of operation (compare or update).
    :param logger: Logger instance for logging purposes.
    """
    actual_image = _handle_mode(page_object, expected_value, mode, logger)
    if actual_image is None:
        return ImageExpectationResult(
            True,
            expected_value,
            expected_value,
            "assert_visual_match_in_regions",
            True,
            logger,
            page_object.__full_name__,
        )

    expect_object = prepare_expect_object(
        page_object, actual_image, True, "Asserting partial visual match.", logger
    )
    return expect_object.to_match_in_specified_regions(
        expected_value, compare_regions, mismatch_threshold
    )


def verify_visual_exclusion_match(
    page_object,
    expected_value: Union[Image, str],
    exclude_regions: Optional[list],
    mismatch_threshold: float,
    mode: VisualModeType,
    logger: Logger,
) -> ImageExpectationResult:
    """
    Verifies the visual match for the web page excluding the specified regions against the expected image.

    :param page_object: The object representing the current web page context.
    :param expected_value: The expected image or path to the expected image for comparison.
    :param exclude_regions: Regions within the image to exclude from the comparison.
    :param mismatch_threshold: The allowable percentage difference excluding the specified regions.
    :param mode: The mode of operation (compare or update).
    :param logger: Logger instance for logging purposes.
    :return: An ImageExpectationResult indicating the outcome of the verification.
    """
    actual_image = _handle_mode(page_object, expected_value, mode, logger)
    if actual_image is None:
        return ImageExpectationResult(
            True,
            expected_value,
            expected_value,
            "verify_visual_exclusion_match",
            False,
            logger,
            page_object.__full_name__,
        )

    expect_object = prepare_expect_object(
        page_object, actual_image, False, "Verifying partial visual match.", logger
    )
    return expect_object.to_match_excluding_regions(
        expected_value, exclude_regions, mismatch_threshold
    )


def assert_visual_exclusion_match(
    page_object,
    expected_value: Union[Image, str],
    exclude_regions: Optional[list],
    mismatch_threshold: float,
    mode: VisualModeType,
    logger: Logger,
) -> ImageExpectationResult:
    """
    Asserts the visual match for the web page excluding the specified regions against the expected image.

    :param page_object: The object representing the current web page context.
    :param expected_value: The expected image or path to the expected image for comparison.
    :param exclude_regions: Regions within the image to exclude from the comparison.
    :param mismatch_threshold: The allowable percentage difference excluding the specified regions.
    :param mode: The mode of operation (compare or update).
    :param logger: Logger instance for logging purposes.
    :return: An ImageExpectationResult indicating the outcome of the assertion.
    """
    actual_image = _handle_mode(page_object, expected_value, mode, logger)
    if actual_image is None:
        return ImageExpectationResult(
            True,
            expected_value,
            expected_value,
            "assert_visual_exclusion_match",
            True,
            logger,
            page_object.__full_name__,
        )

    expect_object = prepare_expect_object(
        page_object, actual_image, True, "Asserting partial visual match.", logger
    )
    return expect_object.to_match_excluding_regions(
        expected_value, exclude_regions, mismatch_threshold
    )
