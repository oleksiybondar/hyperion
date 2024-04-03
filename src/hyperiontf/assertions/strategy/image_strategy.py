from typing import Optional, Union

from .default_strategy import DefaultStrategy
from hyperiontf.image_processing.image import Image
import cv2
import numpy as np
import base64

from hyperiontf.assertions.image_expectation_result import ImageExpectationResult
from ..expectation_result import ExpectationResult
from ...helpers.numeric_helpers import greatest_common_divisor

RED = [0, 0, 255]
"""
A constant representing the color red in BGR format.
Used to highlight actual differences between the compared images,
indicating areas where the actual image deviates from the expected image.
"""

GREEN = [0, 173, 0]
"""
A constant representing a shade of green in BGR format.
Used to highlight expected areas in the difference image,
indicating regions that match the expectations set for the comparison.
"""

PURPLE = [200, 100, 200]
"""
A constant representing a shade of purple in BGR format.
Used to illustrate color discrepancies between the actual and expected images,
marking areas where the colors differ but are not necessarily considered a direct mismatch.
"""

ORANGE = [0, 165, 255]
"""
A constant representing the color orange in BGR format.
Typically used to outline or frame sections of the image or annotations,
helping to draw attention to specific areas or features within the visual comparison.
"""

GRAY = [60, 63, 65]
"""
A constant representing a shade of gray in BGR format.
Often used as a background color in areas of the image that do not directly contribute
to the comparison results but provide context or separation, such as legend backgrounds.
"""

BLUE = [255, 0, 0]
"""
A constant representing the color black in BGR format.
Used to outline or highlight the excluded regions within the image comparison visuals,
indicating areas that are intentionally ignored during the analysis.

This color is applied to demarcate sections or regions within an image that should not
be considered in the comparison process, helping to distinguish these from areas of actual interest.
Typically used in functions generating visual feedback or comparison legends to signify exclusion zones.
"""

BLACK = [0, 0, 0]
"""
A constant representing the color blue in BGR format.
Used to outline or emphasize the regions of interest that are subject to comparison in the image analysis,
signaling areas specifically included for detailed examination.

This color delineates the boundaries of comparison regions, aiding in their visual identification against
the backdrop of the entire image. It is often employed within visualization functions to enhance clarity
and focus on areas under active consideration or analysis.
"""


def convert_path_to_image(method):
    def wrapper(self, expected_value, *args, **kwargs):
        if isinstance(expected_value, str):
            expected_value = Image(expected_value)
        return method(self, expected_value, *args, **kwargs)

    return wrapper


def _generate_diff_image_with_legend(diff_image):
    """
    Generates a difference image with an appended legend at the bottom.

    This function takes a difference image (presumably highlighting areas of mismatch
    between two images being compared) and appends a legend to it. The legend includes
    color-coded keys and descriptions to help interpret the difference visualization.
    Specifically, it annotates red, green, and purple areas to represent actual differences,
    expected similarities, and color discrepancies, respectively. An orange frame is
    added to separate the legend from the image, and a gray background is used for the
    legend for clarity.

    Args:
        diff_image (numpy.ndarray): The initial difference image array without the legend,
                                    typically an image highlighting discrepancies between
                                    the actual and expected images in an image comparison.

    Returns:
        numpy.ndarray: An updated image array that includes the original difference image
                       with an appended legend at the bottom, providing a comprehensive
                       visual context for interpreting the difference visualization.
    """
    height, width, _ = diff_image.shape
    legend_height = 150  # Increased height for separate line for each item
    new_height = height + legend_height
    with_legend = np.full(
        (new_height, width, 3), GRAY, dtype=np.uint8
    )  # Gray filling for legend
    with_legend[:height, :, :] = diff_image  # Copy the original image

    # Draw the orange frame
    cv2.rectangle(
        with_legend, (0, height), (width, new_height), ORANGE, 2
    )  # Orange color

    # Prepare the legend text
    cv2.putText(
        with_legend,
        "Artifacts description:",
        (10, height + 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        ORANGE,
        2,
    )

    # Red square and text for actual differences
    cv2.rectangle(
        with_legend, (10, height + 30), (30, height + 50), RED, -1
    )  # Red square
    cv2.putText(
        with_legend,
        "Changes from actual image",
        (40, height + 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        RED,
        1,
    )

    # Green square and text for expected differences, on a new line
    cv2.rectangle(
        with_legend, (10, height + 70), (30, height + 90), GREEN, -1
    )  # Green square
    cv2.putText(
        with_legend,
        "Expectation",
        (40, height + 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        GREEN,
        1,
    )

    # Bright purple square and text for color discrepancies, on another new line
    cv2.rectangle(
        with_legend, (10, height + 110), (30, height + 130), PURPLE, -1
    )  # Bright purple square
    cv2.putText(
        with_legend,
        "Color discrepancy",
        (40, height + 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        PURPLE,
        1,
    )

    return with_legend


def _generate_diff_image_with_regions_legend(diff_image):
    """
    Appends an additional legend at the bottom of the diff image to describe the excluded and compared regions.

    Args:
        diff_image (numpy.ndarray): The diff image to which the regions legend will be appended.

    Returns:
        numpy.ndarray: The updated diff image with an additional legend for the regions.
    """
    height, width, _ = diff_image.shape
    regions_legend_height = 70  # Define the height of the regions legend area.
    new_height = height + regions_legend_height
    diff_image_with_regions_legend = np.full(
        (new_height, width, 3), GRAY, dtype=np.uint8
    )  # Extend the image with gray background.
    diff_image_with_regions_legend[:height, :, :] = (
        diff_image  # Copy the original diff image.
    )

    # Line positions
    first_line_y = height + 12
    second_line_y = height + 42

    # Blue rectangle for "Regions to be compared"
    cv2.rectangle(
        diff_image_with_regions_legend,
        (10, first_line_y),
        (30, first_line_y + 20),
        BLUE,
        2,
    )

    # Draw the orange frame
    cv2.rectangle(
        diff_image_with_regions_legend, (0, height), (width, new_height), ORANGE, 2
    )  # Orange color

    cv2.putText(
        diff_image_with_regions_legend,
        "Regions to be compared",
        (40, first_line_y + 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        BLUE,
        1,
    )

    # Black rectangle for "Excluded from comparison regions"
    cv2.rectangle(
        diff_image_with_regions_legend,
        (10, second_line_y),
        (30, second_line_y + 20),
        BLACK,
        2,
    )
    cv2.putText(
        diff_image_with_regions_legend,
        "Excluded from comparison regions",
        (40, second_line_y + 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        BLACK,
        1,
    )

    return diff_image_with_regions_legend


def _regions_to_points(region: dict, scale_factor: float):
    """
    Transforms a region's dictionary representation into coordinate points, scaled by a given factor.

    This function takes a region defined by its top-left corner (x, y) and dimensions (width, height),
    and applies a scaling factor to these values to produce scaled coordinates. These coordinates are
    particularly useful for subsequent operations that require precise pixel locations within an image,
    such as annotating, cropping, or analyzing specific areas after image resizing.

    Args:
        region (dict): A dictionary representing a region, containing keys 'x', 'y', 'width', and 'height'.
                       The values should define the region's top-left corner and its size.
        scale_factor (float): A scaling factor to be applied to the region's dimensions and position, typically
                              derived from the ratio between the original image size and the processed image size.

    Returns:
        tuple: A 4-element tuple (x_start, y_start, x_end, y_end) representing the scaled coordinates of the
               region's top-left and bottom-right corners.
    """
    x_start = int(region["x"] * scale_factor)
    y_start = int(region["y"] * scale_factor)
    x_end = x_start + int(region["width"] * scale_factor)
    y_end = y_start + int(region["height"] * scale_factor)
    return x_start, y_start, x_end, y_end


class ImageStrategy(DefaultStrategy):
    """
    A strategy class that extends DefaultStrategy to provide specialized image comparison functionalities
    within an expectation-based testing framework.

    This class is designed to handle image data types, offering a suite of assertion methods to evaluate
    and compare image objects. It supports various comparison operations, including exact matches, similarity
    assessments within a tolerance threshold, detailed difference analysis, and region-specific comparisons.

    The ImageStrategy encapsulates the logic necessary to interpret image comparison outcomes, generate visual
    difference indicators, quantify similarity metrics, and respect region-specific comparison directives,
    facilitating intuitive and informative test results.

    Attributes:
        types (list): A list of supported types that the strategy can handle; this is primarily set to include only Image types.
        actual_value (Image): The actual image that is being tested or compared against an expected value.
        _image_difference (numpy.ndarray): An internal attribute to store the calculated difference between the actual and expected images.
        _actual_working (numpy.ndarray): A copy of the actual image used during comparison operations, which may be altered or processed.
        _expected_working (numpy.ndarray): A processed copy of the expected image used during comparison operations.
        _compare_regions (list): Optional regions within the actual image to focus the comparison on.
        _exclude_regions (list): Optional regions within the actual image to exclude from the comparison.

    Methods:
        to_be(expected_value: Image): Asserts that the actual image should exactly match the expected image.
        not_to_be(expected_value: Image): Asserts that the actual image should not match the expected image.
        to_be_similar(expected_value: Image, mismatch_threshold: int): Asserts that the actual image should
            resemble the expected image within a defined mismatch threshold, optionally considering or ignoring specific regions.
        to_match_in_specified_regions(expected_value: Image, compare_regions: list, mismatch_threshold: int = 0): Asserts
            that specified regions within the actual image match the corresponding regions in the expected image.
        to_match_excluding_regions(expected_value: Image, exclude_regions: list, mismatch_threshold: int = 0): Asserts
            that the actual image, excluding specified regions, matches the expected image.

    The use of this class within a testing framework allows for expressive and detailed assertions on image data,
    supporting nuanced verification of visual content, graphical elements, and attention to or exclusion of particular regions.
    """

    types = [Image]

    def __init__(self, actual_value):
        """
        Initializes the ImageStrategy with the actual image to be compared.

        This constructor sets up the necessary internal state of the ImageStrategy instance
        by storing the actual image and preparing additional attributes that will be used
        in the image comparison processes.

        Args:
            actual_value (Image): The actual image object that will be subjected to various
                                  comparison assertions within the testing framework.
        """
        super().__init__(actual_value)
        self._image_difference = None
        self._expected_value = None
        self._scale_factor = None
        self._actual_working = None
        self._expected_working = None
        # Initialize region fields
        # Reset region fields
        self._compare_regions = None
        self._exclude_regions = None
        self._compare_regions_mask = None
        self._exclude_regions_mask = None

    @convert_path_to_image
    def to_be(self, expected_value: Union[Image, str]) -> ImageExpectationResult:
        """
        Asserts that the actual image exactly matches the expected image in a pixel-perfect manner.

        This method conducts a detailed, pixel-by-pixel comparison between the actual and expected images.
        It first checks if the images are of the same dimensions. If they are, it proceeds to compare each
        corresponding pixel for an exact match. Any discrepancy in pixel data will result in a failed assertion.

        For images with differing dimensions or for cases where specific regions are defined for exclusion or
        focused comparison (if such features are implemented), additional checks or pre-processing steps may be
        involved to appropriately assess equivalency based on the context of the comparison.

        Args:
            expected_value (Image): The expected image to be compared against the actual image. It should be
                                    an instance of the Image class, containing the image data along with any
                                    relevant metadata.

        Returns:
            ImageExpectationResult: An object encapsulating the result of the comparison. This object includes
                                    details such as whether the comparison succeeded (i.e., the images are
                                    identical) and any pertinent data regarding the comparison process or outcome.

        """
        self._initialize_compare_data(expected_value)  # type: ignore # the string path will be auto converted by helper
        comparison_info = self._compare(0)
        return ImageExpectationResult(
            actual_value=self.actual_value,
            expected_value=expected_value,
            processing_data=comparison_info,
            method="to_be",
            result=comparison_info.get("result", False),
        )

    @convert_path_to_image
    def not_to_be(self, expected_value: Union[Image, str]) -> ImageExpectationResult:
        """
        Asserts that the actual image does not exactly match the expected image in a pixel-perfect manner.

        This method compares the actual and expected images to ensure they are not identical. It begins by verifying
        whether the images have the same dimensions. If the dimensions differ, the assertion is immediately considered
        successful without further analysis. However, if the dimensions match, the method performs a pixel-by-pixel
        comparison. The assertion succeeds (indicating the images are not the same) if any pixel differs between the
        two images. If all pixels are identical, the assertion fails.

        The method is particularly useful for cases where distinctiveness between two images is required, such as
        ensuring that an image processing operation has altered the original image or verifying that two images from
        different sources are not the same.

        Args:
            expected_value (Image): The image that the actual image is expected not to match. This should be an
                                    instance of the Image class, containing the image data along with any relevant
                                    metadata.

        Returns:
            ImageExpectationResult: An object encapsulating the result of the comparison. This object includes
                                    information indicating whether the images are not identical, along with any
                                    relevant comparison data or metadata.
        """
        self._initialize_compare_data(expected_value)  # type: ignore # the string path will be auto converted by helper
        comparison_info = self._compare(0)
        return ImageExpectationResult(
            actual_value=self.actual_value,
            expected_value=expected_value,
            processing_data=comparison_info,
            method="not_to_be",
            result=not comparison_info.get("result", False),
        )

    @convert_path_to_image
    def to_be_similar(
        self,
        expected_value: Union[Image, str],
        mismatch_threshold: int,
        compare_regions: Optional[list] = None,
        exclude_regions: Optional[list] = None,
    ) -> ImageExpectationResult:
        """
        Asserts that the actual image is similar to the expected image within a defined mismatch threshold,
        optionally considering or ignoring specific regions for a more targeted comparison.

        This method compares the actual image to the expected image, allowing for a specified degree of variation
        between them as defined by the mismatch_threshold. The comparison can be fine-tuned by specifying regions
        of the image to specifically compare or exclude from the comparison. The comparison algorithm assesses
        similarity on a pixel-by-pixel basis, adjusted for the designated threshold and regional focus.

        The mismatch_threshold parameter defines the acceptable percentage difference between the images, allowing
        for minor variations due to compression artifacts, rendering differences, or other acceptable noise. The
        method supports selective focus through compare_regions and selective ignorance via exclude_regions, enabling
        nuanced comparison scenarios where full image matching is unnecessary or impractical.

        Args:
            expected_value (Image): The expected image to compare against the actual image. It should be an instance
                                    of the Image class, encapsulating the image data along with any relevant metadata.
            mismatch_threshold (int): The permissible percentage difference between the images, representing the
                                      tolerance for discrepancies to still consider the images as similar.
            compare_regions (Optional[list]): Optional list of regions to specifically include in the comparison, with
                                              each region defined as a dictionary containing 'x', 'y', 'width', and 'height'.
            exclude_regions (Optional[list]): Optional list of regions to exclude from the comparison, with each region
                                              similarly defined as a dictionary.

        Returns:
            ImageExpectationResult: An object encapsulating the comparison result, indicating whether the actual image
                                    is considered similar to the expected image within the threshold and any specified
                                    regional focus. The result includes a similarity score and may include a difference
                                    image for visualization.
        """
        self._initialize_compare_data(expected_value, compare_regions, exclude_regions)  # type: ignore # the string path will be auto converted by helper
        comparison_info = self._compare(mismatch_threshold)
        human_readable_description = "Image similarity"
        return ImageExpectationResult(
            actual_value=self.actual_value,
            expected_value=expected_value,
            processing_data=comparison_info,
            method="to_be_similar",
            human_readable_description=human_readable_description,
            result=comparison_info.get("result", False),
        )

    @convert_path_to_image
    def to_match_in_specified_regions(
        self,
        expected_value: Union[Image, str],
        compare_regions: list,
        mismatch_threshold: int = 0,
    ) -> ImageExpectationResult:
        """
        Asserts that selected regions within the actual image match corresponding regions in the expected image,
        within an optional mismatch threshold. This method allows focused comparison on parts of the images that
        are of particular interest, potentially ignoring the rest of the image content.

        The compare_regions argument should be a list of dictionaries, each defining a region with 'x', 'y', 'width',
        and 'height' keys. The comparison assesses each specified region independently, comparing the actual image's
        region against the corresponding region in the expected image. If a mismatch_threshold is provided, minor
        differences between the compared regions up to the specified threshold are tolerated.

        This method is especially useful for scenarios where only certain parts of the image are relevant for
        comparison, allowing testers to specify exactly which regions should match between the actual and expected
        images, thus providing granular control over the comparison process.

        Args:
            expected_value (Image): The expected image to compare against the actual image. It should be an instance
                                    of the Image class, containing the image data along with any relevant metadata.
            compare_regions (list): A list of dictionaries, each specifying a rectangular region in the images to
                                    compare. Each dictionary should have 'x', 'y', 'width', and 'height' keys.
            mismatch_threshold (int, optional): An optional threshold for allowed mismatch percentage within the
                                                 specified regions, defaulting to 0 for an exact match requirement.

        Returns:
            ImageExpectationResult: An object encapsulating the comparison result, indicating whether the specified
                                    regions of the actual image match those in the expected image within the given
                                    tolerance. Includes detailed results for each region compared, and a comprehensive
                                    match assessment.
        """
        self._initialize_compare_data(expected_value, compare_regions=compare_regions)  # type: ignore # the string path will be auto converted by helper
        comparison_info = self._compare(mismatch_threshold)
        human_readable_description = "Images matches in specified regions"
        return ImageExpectationResult(
            actual_value=self.actual_value,
            expected_value=expected_value,
            processing_data=comparison_info,
            method="to_match_in_specified_regions",
            human_readable_description=human_readable_description,
            result=comparison_info.get("result", False),
        )

    @convert_path_to_image
    def to_match_excluding_regions(
        self,
        expected_value: Union[Image, str],
        exclude_regions: list,
        mismatch_threshold: int = 0,
    ) -> ImageExpectationResult:
        """
        Asserts that the actual image matches the expected image, excluding the differences in specified regions,
        within a permissible mismatch threshold. This method allows exclusion of certain image areas from the
        comparison, focusing the match assessment on the remaining regions.

        The exclude_regions argument should be a list of dictionaries, each dictating a region to be excluded with
        'x', 'y', 'width', and 'height' keys. These regions are ignored during the comparison, enabling testers to
        isolate and exclude areas with known or irrelevant differences. The mismatch_threshold parameter allows
        a defined tolerance level for the matching process in the non-excluded areas of the images.

        This functionality is particularly valuable when certain image sections are dynamic or irrelevant to the
        test's intent, enabling precise and focused image analysis that disregards these areas.

        Args:
            expected_value (Image): The expected image to compare against the actual image, encapsulating the image
                                    data along with any pertinent metadata.
            exclude_regions (list): A list of dictionaries, each specifying a rectangular region in the images to
                                    be excluded from the comparison. Each dictionary should define 'x', 'y', 'width',
                                    and 'height' keys.
            mismatch_threshold (int, optional): An optional threshold defining the allowed percentage of mismatch
                                                 in the non-excluded areas, with 0 requiring exact match.

        Returns:
            ImageExpectationResult: An object detailing the comparison results, indicating whether the non-excluded
                                    regions of the actual image match the expected image within the set mismatch
                                    tolerance. The result object provides an aggregate assessment and may include
                                    detailed analysis or visualization data.
        """
        self._initialize_compare_data(expected_value, exclude_regions=exclude_regions)  # type: ignore # the string
        # path will be auto converted by helper
        comparison_info = self._compare(mismatch_threshold)
        human_readable_description = (
            "Images partially matching, excluding specified regions"
        )
        return ImageExpectationResult(
            actual_value=self.actual_value,
            expected_value=expected_value,
            processing_data=comparison_info,
            method="to_match_excluding_regions",
            human_readable_description=human_readable_description,
            result=comparison_info.get("result", False),
        )

    def to_exist(self) -> ExpectationResult:
        """
        Asserts that the file or directory exists.

        Returns:
            ExpectationResult: The result of the assertion.
        """
        result = self.actual_value.exists()
        message = "Expected to exist."
        return ExpectationResult(
            result=result,
            actual_value=str(self.actual_value),
            expected_value=None,
            method="to_exist",
            human_readable_description=message,
        )

    def not_to_exist(self) -> ExpectationResult:
        """
        Asserts that the file or directory does not exist.

        Returns:
            ExpectationResult: The result of the assertion.
        """
        result = not self.actual_value.exists()
        message = "Expected not to exist."
        return ExpectationResult(
            result=result,
            actual_value=str(self.actual_value),
            expected_value=None,
            method="not_to_exist",
            human_readable_description=message,
        )

    def _compare(self, mismatch_threshold: float = 10.0) -> dict:
        """
        Compares the actual image with the expected image based on the given mismatch threshold.

        This method initiates the comparison process by generating an image difference object and then
        uses this object to evaluate whether the images are sufficiently similar based on the mismatch
        threshold. It calculates a match score that quantifies the similarity between the two images
        and determines the comparison result based on whether this score meets or exceeds the threshold
        set for acceptable similarity.

        The comparison considers the whole image by default, but it can also focus on specific regions
        or exclude certain areas from consideration if the corresponding masks have been defined. The
        method returns a dictionary containing detailed information about the comparison, including the
        success status, match score, and potentially a difference image highlighting the disparities.

        Args:
            mismatch_threshold (float): The maximum allowed mismatch percentage between the images.
                                        Defaults to 10.0, meaning up to 10% difference is acceptable.

        Returns:
            dict: A dictionary containing detailed results of the comparison. Key information includes:
                  - 'result': A boolean indicating whether the images are considered similar within the
                              defined threshold.
                  - 'match_score': The calculated similarity score between the images.
                  - Additional keys providing context and details about the comparison process and outcome.
        """
        self._make_image_diff_object()

        comparison_info = self._make_comparison_info(mismatch_threshold)
        self._cleanup()
        return comparison_info

    def _make_comparison_info(self, mismatch_threshold: float) -> dict:
        """
        Generates a detailed summary of the image comparison results.

        This method calculates a match score to quantify the similarity between the actual and expected images,
        considering the given mismatch threshold. It determines whether the images are deemed similar based on
        the score and threshold, and compiles various metrics and flags that describe the nature and context of
        the comparison. The result includes the overall success of the comparison, whether the images are proportional,
        if they were scaled, the type of comparison (pixel-perfect or not), and whether regions were specifically
        compared or excluded.

        The method also generates a visual representation of the differences if applicable, and incorporates
        all this information into a dictionary that provides a comprehensive overview of the comparison outcome.

        Args:
            mismatch_threshold (float): The maximum allowed mismatch percentage used to evaluate the image similarity.

        Returns:
            dict: A dictionary containing the comparison results and details, including:
                  - 'result': A boolean indicating if the images are similar within the specified threshold.
                  - 'proportional': A boolean indicating if the actual and expected images are proportional.
                  - 'scaled': A boolean indicating if scaling was applied to the images during comparison.
                  - 'pixel_perfect': A boolean indicating if a pixel-perfect comparison was requested.
                  - 'partial': A boolean indicating if the comparison was limited to specified regions.
                  - 'height', 'width', 'ratio': Dimensions and aspect ratio of the compared images.
                  - 'difference_image': A base64-encoded string of the difference image, if generated.
                  - 'match_score': The calculated similarity score between the images.
        """
        match_score = self._calculate_match_score()
        pixel_perfect = mismatch_threshold == 0
        if pixel_perfect:
            result = self._is_pixel_perfect(match_score)
        else:
            result = match_score >= (100 - mismatch_threshold)

        return {
            "result": result,
            "proportional": self._are_images_proportional(),
            "scaled": self._scale_factor != 1,
            "pixel_perfect": pixel_perfect,
            "partial": self._has_regions,
            "height": self._height,
            "width": self._width,
            "ratio": self._ratio,
            "difference_image": self._generate_difference_image(),
            "match_score": match_score,
        }

    def _calculate_match_score(self):
        """
        Calculates a similarity score based on the differences between the actual and expected images.

        This method assesses the pixel-wise differences captured in the _image_difference attribute to
        quantify how similar the actual and expected images are. The score is a percentage value where 100%
        signifies identical images, and lower values indicate increasing dissimilarity.

        The calculation considers only the regions of interest, which are determined by the presence of compare
        and exclude regions if they have been defined. The score reflects the proportion of pixels that are similar
        within the included regions, adjusted to provide a percentage value.

        No input parameters are required, as the method operates based on the internal state of the class.

        Returns:
            float: The calculated match score, ranging from 0.0 to 100.0, where 100.0 represents identical images,
                   and lower values indicate greater dissimilarity.
        """
        # Create a mask initialized to false (exclude everything)
        mask = np.zeros(self._image_difference.shape[:2], dtype=bool)

        # If compare regions are specified, set those regions in the mask to true (include them)
        if self._compare_regions_mask is not None:
            mask |= self._compare_regions_mask

        # If no compare regions are specified, include the entire image
        if self._compare_regions_mask is None:
            mask[:] = True

        # Exclude the specified exclude regions from the mask
        if self._exclude_regions_mask is not None:
            mask &= ~self._exclude_regions_mask

        # Calculate the match score only using the included regions
        included_diff = self._image_difference[mask]
        score = 100 - (np.mean(included_diff) * 100 / 255)

        return score

    def _make_image_diff_object(self):
        """
        Generates an object representing the pixel-wise differences between the actual and expected images.

        This method computes the absolute differences between corresponding pixels in the actual and expected images,
        resulting in a new image that highlights these differences. The resultant difference image is stored internally
        and used for subsequent similarity assessment and visualization.

        The method also prepares masks based on the specified regions to compare or exclude, if any. These masks ensure that
        the comparison and subsequent analyses focus on the relevant portions of the images while ignoring the designated
        regions for exclusion. The outcome is a detailed representation of the differences that respects the contextual
        constraints defined by any specified regions.

        No input parameters are required as the method operates on the internal state of the class, utilizing the actual
        and expected image data along with any defined compare or exclude regions.

        Returns:
            numpy.ndarray: The computed image difference, highlighting the disparities between the actual and expected
                           images while considering any specified regions for focused comparison or exclusion.
        """
        # Calculate difference and match score.
        self._image_difference = cv2.absdiff(
            self._actual_working, self._expected_working
        )

        # If no compare regions are specified, assume the comparison includes the whole image.
        if self._compare_regions_mask is None:
            included_pixels_mask = np.ones(self._actual_working.shape[:2], dtype=bool)
        else:
            # Use the compare regions mask directly since it should already be a boolean array.
            included_pixels_mask = self._compare_regions_mask

        # Exclude the specified exclude regions from the included pixels mask.
        if self._exclude_regions_mask is not None:
            included_pixels_mask &= ~self._exclude_regions_mask

        # Apply the mask to the image difference, ensuring the mask is correctly expanded for all color channels.
        included_pixels_mask_3d = np.repeat(
            included_pixels_mask[:, :, np.newaxis], 3, axis=2
        )
        self._image_difference[~included_pixels_mask_3d] = 0

        return self._image_difference

    def _generate_difference_image(self):
        """
        Creates an image that visually illustrates the differences between the actual and expected images.

        This method generates a difference image where discrepancies between the actual and expected images
        are highlighted in distinct colors. It visualizes the differences by applying color coding to various
        types of discrepancies: areas with significant changes are marked in one color, expected regions in another,
        and potential color discrepancies are indicated with a third color. This visual differentiation helps in
        understanding the nature and locations of the differences.

        The method also appends a legend to the difference image, providing explanations for each color code,
        thereby making the image self-explanatory. In cases where specific regions have been compared or excluded,
        the method also overlays these regions onto the difference image for a clear and comprehensive presentation.

        No input parameters are required, as the method operates on the internal state of the class, specifically
        utilizing the computed image differences and the context provided by any specified compare or exclude regions.

        Returns:
            str: A base64-encoded string representing the difference image with an appended legend, suitable for
                 embedding in reports or web pages to visually communicate the comparison results.
        """
        diff_image = self._generate_base_difference_image()

        self._overlay_region_rectangles(diff_image)
        diff_image = _generate_diff_image_with_legend(diff_image)

        if self._has_regions:
            diff_image = _generate_diff_image_with_regions_legend(diff_image)

        # Convert to base64 for consistency
        _, buffer = cv2.imencode(".png", diff_image)
        base64_image = base64.b64encode(buffer).decode("utf-8")

        return f"data:image/png;base64,{base64_image}"

    def _cleanup(self):
        """
        Resets the internal state of the class after a comparison operation.

        This method clears out the internal attributes used during the image comparison process, including
        the working copies of the actual and expected images, the image difference data, and any scale factors
        or region-specific masks that were applied. Resetting these attributes ensures that they do not affect
        subsequent comparisons and that each comparison starts with a fresh state.

        The method does not require any input parameters and does not return any values. It directly modifies
        the internal state of the instance, clearing the relevant attributes to prepare for the next image
        comparison operation.
        """
        self._expected_value = None
        self._actual_working = None
        self._expected_working = None
        self._image_difference = None
        self._scale_factor = None
        # Reset region fields
        self._compare_regions = None
        self._exclude_regions = None
        self._compare_regions_mask = None
        self._exclude_regions_mask = None

    def _generate_base_difference_image(self):
        """
        Produces a grayscale image highlighting the differences between the actual and expected images.

        This method computes the absolute differences between corresponding pixels in the actual and expected images,
        resulting in a grayscale image where the intensity of each pixel corresponds to the magnitude of the difference
        at that location. Areas of significant discrepancy appear brighter, providing a visual cue to their presence and
        magnitude.

        Following the generation of this base difference image, further processing can apply color coding to indicate
        different types of discrepancies or to overlay region-specific annotations. The resulting image serves as a
        foundational element for detailed analysis and visualization of the differences.

        The method does not require input parameters and operates based on the internal state of the class, utilizing the
        processed actual and expected image data.

        Returns:
            numpy.ndarray: An array representing the base grayscale difference image, which visually encodes the
                           pixel-wise discrepancies between the actual and expected images.
        """
        # Calculate the absolute difference and create masks for various types of discrepancies
        actual_diff_gray = cv2.cvtColor(self._image_difference, cv2.COLOR_BGR2GRAY)

        # Detect significant changes from the actual image
        _, actual_diff_thresh = cv2.threshold(
            actual_diff_gray, 90, 255, cv2.THRESH_BINARY
        )
        actual_mask_diff = actual_diff_thresh > 0

        # Detect expected differences excluding the actual differences
        expected_mask_diff = (
            cv2.cvtColor(self._image_difference, cv2.COLOR_BGR2GRAY) > 30
        ) & ~actual_mask_diff

        # Identify color discrepancies excluding both actual and expected differences
        color_mask_diff = (
            (cv2.cvtColor(self._image_difference, cv2.COLOR_BGR2GRAY) > 15)
            & ~actual_mask_diff
            & ~expected_mask_diff
        )

        # Apply masks to the final image with designated colors
        diff_image = self._expected_working.copy()
        diff_image[actual_mask_diff] = (
            GREEN  # Green for actual differences, e.g. highlights what was expected
        )
        diff_image[expected_mask_diff] = (
            RED  # Red for expected differences, e.g. highlights what was changed
        )
        diff_image[color_mask_diff] = PURPLE  # Bright purple for color differences

        return diff_image

    def _are_images_proportional(self):
        """
        Determines whether the actual and expected images have proportional dimensions, based on their aspect ratios.

        This method compares the aspect ratios of the actual and expected images to check if they are the same,
        indicating that the images are proportional. Proportionality is a significant factor in image comparisons,
        especially when resizing images for non-pixel-perfect comparisons. Ensuring that images are proportional
        allows for more accurate and meaningful comparisons, as it maintains the integrity of the visual content
        during scaling operations.


        Returns:
            bool: True if the actual and expected images have the same aspect ratio and are therefore proportional,
                  False otherwise.
        """
        return self.actual_value.aspect_ratio == self._expected_value.aspect_ratio

    def _initialize_compare_data(
        self,
        expected_value: Image,
        compare_regions: Optional[list] = None,
        exclude_regions: Optional[list] = None,
    ):
        """
        Prepares and initializes the necessary data for comparing the actual and expected images.

        This method sets up the comparison by storing the expected image and creating working copies of both the
        actual and expected images for processing. It calculates a scale factor to adjust the size of the images
        if necessary, ensuring that they are comparable. The method also processes any specified regions to focus
        the comparison on particular areas or to exclude them from consideration.

        The compare and exclude regions, if provided, are converted into masks that will be used during the comparison
        process to include or ignore specific image areas. These preparations facilitate a focused and relevant comparison
        based on the provided parameters.

        Args:
            expected_value (Image): The expected image to be compared against the actual image.
            compare_regions (Optional[list]): A list of dictionaries defining regions to include in the comparison. Each
                                              dictionary should contain 'x', 'y', 'width', and 'height' keys.
            exclude_regions (Optional[list]): A list of dictionaries defining regions to exclude from the comparison. Each
                                              dictionary should contain 'x', 'y', 'width', and 'height' keys.

        The method does not return any values but updates the internal state of the class to be ready for the image comparison.
        """
        self._expected_value = expected_value
        self._copy_images_before_processing()
        self._remove_alpha_channels()
        self._calculate_scale_factor()
        self._resize_working_images()
        self._compare_regions = compare_regions
        self._exclude_regions = exclude_regions
        self._compare_regions_mask = (
            self._create_regions_mask(compare_regions) if compare_regions else None
        )
        self._exclude_regions_mask = (
            self._create_regions_mask(exclude_regions) if exclude_regions else None
        )

    def _create_regions_mask(self, regions: list):
        """
        Creates a binary mask from specified regions to include or exclude parts of an image during comparison.

        This method constructs a mask where each pixel's value indicates whether it belongs to one of the specified regions.
        The regions are defined as dictionaries containing 'x', 'y', 'width', and 'height' keys, which represent rectangular
        areas within the image. The mask is used in subsequent comparison processes to selectively consider or ignore these
        areas, depending on whether they are designated as regions to compare or exclude.

        The generated mask is particularly useful for focusing the comparison on relevant image areas or excluding regions
        with known, acceptable differences, thus allowing for more targeted and meaningful image comparisons.

        Args:
            regions (list): A list of dictionaries, each defining a rectangular region within the image. Each dictionary
                            should include 'x', 'y', 'width', and 'height' keys to specify the region's location and size.

        Returns:
            np.ndarray: A binary mask array where the presence of a '1' (True) indicates inclusion and '0' (False) indicates
                        exclusion of the corresponding pixel in the image comparison process.
        """
        # Create an empty mask with the same dimensions as the image, initialized to False
        mask = np.zeros((self._height, self._width), dtype=bool)

        # Process each region, updating the mask
        for region in regions:
            if all(key in region for key in ["x", "y", "width", "height"]):
                x_start, y_start, x_end, y_end = _regions_to_points(
                    region, self._scale_factor
                )

                # Set the mask to True within the region
                mask[y_start:y_end, x_start:x_end] = True
            else:
                raise ValueError(
                    "Each region dictionary must contain x, y, width, and height keys."
                )

        return mask

    def _copy_images_before_processing(self):
        """
        Creates working copies of the actual and expected images for processing.

        This method duplicates the actual and expected images to protect the originals from any modifications during
        the comparison process. The comparison operations, such as scaling and applying masks, are performed on these
        copies to prevent altering the input images. This approach maintains the integrity of the original data and
        allows for non-destructive analysis.

        The method does not require input parameters and does not return any values. It updates the internal state
        of the class, specifically initializing the '_actual_working' and '_expected_working' attributes with the
        copies of the actual and expected images, respectively.
        """
        self._actual_working = self.actual_value.image.copy()
        self._expected_working = self._expected_value.image.copy()

    def _calculate_scale_factor(self):
        """
        Calculates the scale factor required to resize the expected image for comparison.

        This method determines the scale factor by comparing the dimensions of the actual and expected images. It ensures
        that the expected image is scaled appropriately to match the size of the actual image, facilitating a pixel-wise
        comparison. The scale factor is calculated as the minimum of the width and height ratios between the actual and
        expected images, maintaining the aspect ratio of the expected image while resizing.

        The method updates the internal '_scale_factor' attribute with the calculated value. This scale factor is then
        used to resize the expected image in the image comparison process.

        No input parameters are required, as the method operates on the internal state of the class, specifically using
        the dimensions of the 'actual_value' and '_expected_value' images to calculate the scaling necessary.

        The method does not return any values but updates the internal '_scale_factor' attribute with the calculated scale factor.
        """
        scale_factor_width = (
            self._actual_working.shape[1] / self._expected_working.shape[1]
        )
        scale_factor_height = (
            self._actual_working.shape[0] / self._expected_working.shape[0]
        )
        self._scale_factor = min(scale_factor_width, scale_factor_height)

    def _resize_working_images(self):
        """
        Resizes the working copies of the actual and expected images to ensure they are the same dimensions.

        This method uses the calculated scale factor to resize the expected image, aligning its dimensions with those
        of the actual image to facilitate a pixel-by-pixel comparison. If the actual and expected images are already the
        same size, this method ensures that both images are still set as the working copies without further modifications.

        The resizing maintains the aspect ratio of the expected image and adjusts its size according to the scale factor
        determined previously. This process is crucial for accurate image comparison, especially when dealing with images
        of different original sizes.

        The method operates on the internal state of the class, updating the '_actual_working' and '_expected_working'
        attributes to hold the resized image data. It ensures that both images are ready for the subsequent comparison steps.

        No input parameters are required, and the method does not return any values. It modifies the '_actual_working' and
        '_expected_working' attributes directly, preparing them for the comparison process.
        """
        # Resize expected working image based on the scale factor
        self._expected_working = cv2.resize(
            self._expected_working,
            None,
            fx=self._scale_factor,
            fy=self._scale_factor,
            interpolation=cv2.INTER_AREA,
        )

        # Retrieve dimensions of the resized expected working image
        height, width = self._expected_working.shape[:2]

        # Resize actual working image to match the dimensions of the expected working image
        self._actual_working = cv2.resize(
            self._actual_working,
            (width, height),
            interpolation=cv2.INTER_AREA,
        )

    @property
    def _width(self):
        """
        Gets the width of the image.

        Returns:
            int: The width of the image in pixels, or None if no image is loaded.
        """
        return (
            self._expected_working.shape[1]
            if self._expected_working is not None
            else None
        )

    @property
    def _height(self):
        """
        Gets the height of the image.

        Returns:
            int: The height of the image in pixels, or None if no image is loaded.
        """
        return (
            self._expected_working.shape[0]
            if self._expected_working is not None
            else None
        )

    @property
    def _ratio(self) -> str:
        """
        Calculates and returns the simplified aspect ratio of the images.

        This property computes the aspect ratio of the images based on their width and height, reducing it to its simplest
        form by finding the greatest common divisor and dividing both dimensions by it. The aspect ratio is essential for
        various comparison operations, ensuring that images are compared accurately and proportionally.

        The aspect ratio is calculated from the dimensions of the '_expected_working' image, which is assumed to have been
        resized or prepared for direct comparison with the actual image.

        Returns:
            str: A string representing the simplified aspect ratio of the image, formatted as 'width:height'.
        """
        width, height = self._width, self._height
        divisor = greatest_common_divisor(width, height)
        simplified_width = width // divisor
        simplified_height = height // divisor

        return f"{simplified_width}:{simplified_height}"

    @property
    def _has_regions(self):
        """
        Checks whether any specific regions have been defined for focused comparison or exclusion.

        This property evaluates whether there are any compare or exclude regions specified for the image comparison process.
        If either the '_compare_regions' or '_exclude_regions' attributes is populated, it indicates that the comparison
        should consider or ignore specific areas of the images, affecting how the comparison is conducted.

        The presence of defined regions enables more granular control over the comparison, allowing for targeted analysis
        or the omission of known-irrelevant or variable areas from the evaluation.

        Returns:
            bool: True if there are specific regions defined for comparison or exclusion; False otherwise.
        """
        return self._compare_regions is not None or self._exclude_regions is not None

    def _is_pixel_perfect(self, match_score: float) -> bool:
        """
        Determines if the comparison between the actual and expected images indicates a pixel-perfect match.

        This method evaluates the match score and the contextual details of the images being compared to determine if they
        match perfectly on a pixel-by-pixel basis. A pixel-perfect match requires not only a 100% match score but also that
        the images have the same dimensions and aspect ratios. This method is critical for scenarios where an exact match is
        necessary, such as validating graphical outputs or confirming image processing results.

        The comparison is deemed pixel-perfect if the match score is 100, and the aspect ratios and dimensions of the actual
        and expected images are identical, ensuring that there is no discrepancy even at the pixel level.

        Args:
            match_score (float): The calculated match score representing the similarity between the actual and expected images.

        Returns:
            bool: True if the images are considered to be a pixel-perfect match; False otherwise.
        """
        if (
            self.actual_value.aspect_ratio != self._expected_value.aspect_ratio
            or self.actual_value.height != self._expected_value.height
            or self.actual_value.width != self._expected_value.width
            or self.actual_value.has_alpha != self._expected_value.has_alpha
        ):
            return False

        return match_score == 100

    def _overlay_region_rectangles(self, diff_image: np.ndarray):
        """
        Overlays rectangles on the difference image to visualize the compare and exclude regions.

        Args:
            diff_image (numpy.ndarray): The difference image on which to overlay the region rectangles.

        Returns:
            numpy.ndarray: The updated difference image with overlay rectangles.
        """
        self._overlay_comparison_areas(diff_image)
        self._overlay_excluded_areas(diff_image)

    def _overlay_comparison_areas(self, diff_image: np.ndarray):
        """
        Draws rectangles on the difference image to indicate the areas designated for comparison.

        This method iterates over the regions specified for comparison and draws blue rectangles around these areas
        on the difference image. These annotations visually demarcate the regions that were specifically included
        in the comparison process, aiding in the interpretation of the difference image by highlighting areas of focus.

        Args:
            diff_image (np.ndarray): The difference image on which to overlay the comparison area annotations.

        The method does not return any values. It modifies the diff_image in-place, adding blue rectangles to indicate
        the regions where the comparison was explicitly performed.
        """
        # Draw blue rectangles for compare regions.
        if self._compare_regions is not None:
            for region in self._compare_regions:
                x_start, y_start, x_end, y_end = _regions_to_points(
                    region, self._scale_factor
                )
                cv2.rectangle(
                    diff_image,
                    (x_start, y_start),
                    (x_end, y_end),
                    BLUE,
                    2,
                )

    def _overlay_excluded_areas(self, diff_image: np.ndarray):
        """
        Draws rectangles and crosshatching on the difference image to indicate the areas designated for exclusion.

        This method iterates over the regions specified for exclusion and draws black rectangles around these areas
        on the difference image. To further emphasize their exclusion, it adds a crosshatching pattern within these
        rectangles. These visual cues help in understanding the difference image by clearly indicating areas that were
        intentionally ignored in the comparison process.

        The crosshatching within the excluded areas provides a clear visual distinction, ensuring that these regions
        are easily recognizable and their exclusion is unambiguous.

        Args:
            diff_image (np.ndarray): The difference image on which to overlay the exclusion area annotations.

        The method does not return any values. It modifies the diff_image in-place, adding black rectangles and
        crosshatching to denote the regions that were excluded from the comparison.
        """
        if self._exclude_regions is not None:
            for region in self._exclude_regions:
                x_start, y_start, x_end, y_end = _regions_to_points(
                    region, self._scale_factor
                )
                cv2.rectangle(
                    diff_image,
                    (x_start, y_start),
                    (x_end, y_end),
                    BLACK,
                    2,
                )

                line_spacing = 10

                # Determine spacing between the lines (you can adjust this value)
                current_pos = x_start + line_spacing
                while current_pos < x_end:
                    start_point = (current_pos, y_start)
                    end_point = (current_pos - line_spacing, y_end)
                    cv2.line(diff_image, start_point, end_point, BLACK, 1)
                    current_pos += line_spacing

    def _remove_alpha_channels(self):
        # Check if the actual image has an alpha channel and remove it
        if self._actual_working.shape[2] == 4:
            self._actual_working = cv2.cvtColor(
                self._actual_working, cv2.COLOR_BGRA2BGR
            )

        # Check if the expected image has an alpha channel and remove it
        if self._expected_working.shape[2] == 4:
            self._expected_working = cv2.cvtColor(
                self._expected_working, cv2.COLOR_BGRA2BGR
            )
