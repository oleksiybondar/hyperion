from typing import Optional, Union
from .automation_adapter_manager import AutomationAdaptersManager
from .action_builder import ActionBuilder
from hyperiontf.image_processing.image import Image
from hyperiontf.assertions.image_expectation_result import ImageExpectationResult
from hyperiontf.configuration import config
from hyperiontf.typing import VisualModeType
from hyperiontf.ui.helpers.visual import (
    verify_visual_match,
    verify_visual_exclusion_match,
    verify_visual_match_in_regions,
)
from hyperiontf.ui.helpers.visual import (
    assert_visual_match,
    assert_visual_match_in_regions,
    assert_visual_exclusion_match,
)


class BasePageObject:
    def __init__(self, automation_descriptor, logger):
        self.automation_adapter = automation_descriptor
        self.__full_name__ = self.__class__.__name__
        self.logger = logger

    @property
    def root(self):
        return self

    @property
    def action_builder(self) -> ActionBuilder:
        builder = ActionBuilder(self.automation_adapter.action_builder)
        builder.sender = self.__full_name__
        builder.logger = self.logger
        return builder

    def quit(self):
        self.logger.info(f"[{self.__full_name__}] Quitting the browser")
        self.automation_adapter.quit()
        AutomationAdaptersManager().delete(self.automation_adapter)

    def make_screenshot(self, filepath: Optional[str] = None) -> Image:
        return Image(
            path=filepath, img_data=self.automation_adapter.screenshot_as_base64
        )

    def screenshot(
        self,
        message: Optional[str] = "Screenshot",
        title: Optional[str] = "Regular screenshot",
    ):
        self.logger.info(
            message,
            extra={
                "attachments": [
                    {
                        "title": title,
                        "type": "image",
                        "url": self.make_screenshot().to_base64(),
                    }
                ]
            },
        )

    def verify_visual_match(
        self,
        expected_value: Union[Image, str],
        mismatch_threshold: float = config.visual.default_mismatch_threshold,
        compare_regions: Optional[list] = None,
        exclude_regions: Optional[list] = None,
        mode: VisualModeType = config.visual.mode,
    ) -> ImageExpectationResult:
        """
        Verifies that the current visual state matches the expected visual reference within the defined mismatch threshold.
        This method supports optional focusing on specific regions for comparison or exclusion, depending on the test's needs.

        Args:
            expected_value (Union[Image, str]): The expected image or a path to the image file against which the actual image is compared.
            mismatch_threshold (float): The allowable percentage difference between the images to consider them as matching.
            compare_regions (Optional[list]): A list of regions (dictionaries with 'x', 'y', 'width', and 'height' keys) to exclusively compare.
            exclude_regions (Optional[list]): A list of regions to exclude from the comparison.
            mode (VisualModeType): The mode of operation (collect or compare) which can override the default behavior.

        Returns:
            ImageExpectationResult: The result of the visual comparison, including a similarity score and potential difference image.
        """
        return verify_visual_match(
            self,
            expected_value,
            mismatch_threshold,
            compare_regions,
            exclude_regions,
            mode,
            self.logger,
        )

    def assert_visual_match(
        self,
        expected_value: Union[Image, str],
        mismatch_threshold: float = config.visual.default_mismatch_threshold,
        compare_regions: Optional[list] = None,
        exclude_regions: Optional[list] = None,
        mode: VisualModeType = config.visual.mode,
    ) -> ImageExpectationResult:
        """
        Asserts that the current visual state matches the expected visual reference within a defined mismatch threshold.
        Allows focusing on or excluding specific regions for comparison, providing flexibility for varied testing needs.

        Args:
            expected_value (Union[Image, str]): The expected image or path to the image file for comparison.
            mismatch_threshold (float): The permissible percentage difference between the images for a successful match.
            compare_regions (Optional[list]): Specific regions to compare, defined as dictionaries with coordinates and dimensions.
            exclude_regions (Optional[list]): Regions to be excluded from the comparison.
            mode (VisualModeType): The mode setting which determines the behavior (collect or compare).

        Returns:
            ImageExpectationResult: The outcome of the visual assertion, including details on similarity and any differences.
        """
        return assert_visual_match(
            self,
            expected_value,
            mismatch_threshold,
            compare_regions,
            exclude_regions,
            mode,
            self.logger,
        )

    def verify_visual_match_in_regions(
        self,
        expected_value: Union[Image, str],
        compare_regions: Optional[list] = None,
        mismatch_threshold: float = config.visual.default_partial_mismatch_threshold,
        mode: VisualModeType = config.visual.mode,
    ):

        return verify_visual_match_in_regions(
            self, expected_value, compare_regions, mismatch_threshold, mode, self.logger
        )

    def assert_visual_match_in_regions(
        self,
        expected_value: Union[Image, str],
        compare_regions: Optional[list] = None,
        mismatch_threshold: float = config.visual.default_partial_mismatch_threshold,
        mode: VisualModeType = config.visual.mode,
    ):
        """
        Verifies that designated regions within the visual state match the expected reference, considering an optional mismatch threshold.
        This method is particularly useful for tests that target specific areas of the visual representation.

        Args:
            expected_value (Union[Image, str]): The reference image or path to the image file for focused comparison.
            compare_regions (list): The regions within the image to compare, each defined with 'x', 'y', 'width', and 'height'.
            mismatch_threshold (float): The allowed variance percentage between the specified regions of the images.
            mode (VisualModeType): The operational mode (collect or compare) affecting the method's behavior.

        Returns:
            ImageExpectationResult: Detailed results of the region-specific visual comparison.
        """
        return assert_visual_match_in_regions(
            self, expected_value, compare_regions, mismatch_threshold, mode, self.logger
        )

    def verify_visual_exclusion_match(
        self,
        expected_value: Union[Image, str],
        exclude_regions: Optional[list] = None,
        mismatch_threshold: float = config.visual.default_mismatch_threshold,
        mode: VisualModeType = config.visual.mode,
    ) -> ImageExpectationResult:
        """
        Verifies the visual match excluding certain regions, ideal for ignoring known variabilities or non-relevant sections.
        Offers a way to concentrate verification on stable, significant areas of the visual content.

        Args:
            expected_value (Union[Image, str]): The reference image or path for the exclusion-based comparison.
            exclude_regions (Optional[list]): Regions to omit during the verification, specified with their coordinates and dimensions.
            mismatch_threshold (float): Permitted percentage of difference in the non-excluded image areas.
            mode (VisualModeType): The running mode (collect or compare), influencing the execution context.

        Returns:
            ImageExpectationResult: The outcome of the comparison, emphasizing the non-excluded areas.
        """
        return verify_visual_exclusion_match(
            self, expected_value, exclude_regions, mismatch_threshold, mode, self.logger
        )

    def assert_visual_exclusion_match(
        self,
        expected_value: Union[Image, str],
        exclude_regions: Optional[list] = None,
        mismatch_threshold: float = config.visual.default_mismatch_threshold,
        mode: VisualModeType = config.visual.mode,
    ) -> ImageExpectationResult:
        """
        Asserts a visual match while disregarding specified regions, suitable for bypassing dynamic or irrelevant image parts.
        Enhances test accuracy by focusing assertions on essential and predictable image segments.

        Args:
            expected_value (Union[Image, str]): The expected image or file path for focused exclusion assertion.
            exclude_regions (Optional[list]): Areas to exclude, each defined by 'x', 'y', 'width', and 'height'.
            mismatch_threshold (float): Acceptance threshold for variations outside the excluded regions.
            mode (VisualModeType): Configuration setting to switch between collect and compare modes.

        Returns:
            ImageExpectationResult: Detailed assertion results, highlighting the examined image portions.
        """
        return assert_visual_exclusion_match(
            self, expected_value, exclude_regions, mismatch_threshold, mode, self.logger
        )
