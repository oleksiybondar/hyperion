from .default_strategy import DefaultStrategy
from hyperiontf.image_processing.image import Image
import cv2
import numpy as np
import base64

from hyperiontf.assertions.image_expectation_result import ImageExpectationResult

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
        "Added in actual image",
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
        "Missing from expected image",
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


class ImageStrategy(DefaultStrategy):
    """
    A strategy class that extends DefaultStrategy to provide specific image comparison
    functionalities within an expectation-based testing framework.

    This class is designed to handle image data types, offering a suite of assertion methods
    to evaluate and compare image objects. It supports various comparison operations,
    including exact matches, similarity assessments within a tolerance threshold, and
    detailed difference analysis. The ImageStrategy encapsulates the logic necessary to
    interpret image comparison outcomes, generate visual difference indicators, and
    quantify similarity metrics, facilitating intuitive and informative test results.

    The class utilizes color-coded difference visualizations to illustrate discrepancies
    between actual and expected images, and includes a method to append a legend to these
    visualizations for enhanced interpretability.

    Attributes:
        types (list): A list of supported types that the strategy can handle; this is
                      primarily set to include only Image types.
        actual_value (Image): The actual image that is being tested or compared against an expected value.
        _image_difference (numpy.ndarray): An internal attribute to store the calculated difference
                                           between the actual and expected images.
        _actual_working (numpy.ndarray): A copy of the actual image used during comparison operations,
                                         which may be altered or processed.
        _expected_working (numpy.ndarray): A processed copy of the expected image used during
                                           comparison operations.

    Methods:
        to_be(expected_value: Image): Asserts that the actual image should exactly match the expected image.
        not_to_be(expected_value: Image): Asserts that the actual image should not match the expected image.
        to_be_similar(expected_value: Image, mismatch_threshold: int): Asserts that the actual image should
                                                                       resemble the expected image within a
                                                                       defined mismatch threshold.
        _compare(expected_value: Image, mismatch_threshold: float): A private method to perform the core
                                                                     comparison logic between the actual and
                                                                     expected images.
        _generate_diff_image_with_legend(diff_image: numpy.ndarray): Enhances a given difference image with
                                                                     a descriptive legend to elucidate the
                                                                     types of discrepancies identified.

    Usage of this class within a testing framework allows for expressive and detailed assertions on image
    data, supporting nuanced verification of visual content and graphical elements.
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
        self._actual_working = None
        self._expected_working = None

    def to_be(self, expected_value: Image) -> ImageExpectationResult:
        """
        Asserts that the actual image exactly matches the expected image in a pixel-perfect manner.

        This method first checks the metadata (height and width) of the actual and expected images.
        If these metadata attributes do not match, the comparison is immediately deemed unsuccessful,
        and no further visual comparison is conducted. If the metadata do match, a detailed, pixel-by-pixel
        comparison is performed to ensure that the actual image is identical to the expected image in every aspect.

        Args:
            expected_value (Image): The expected image to compare against the actual image.

        Returns:
            ImageExpectationResult: An object containing the result of the comparison, detailing whether the
                                    actual image matches the expected image exactly and providing relevant
                                    comparison metadata.
        """
        comparison_info = self._compare(expected_value, 0)
        return ImageExpectationResult(
            actual_value=self.actual_value,
            expected_value=expected_value,
            processing_data=comparison_info,
            method="to_be",
            result=comparison_info.get("result", False),
        )

    def not_to_be(self, expected_value: Image) -> ImageExpectationResult:
        """
        Asserts that the actual image does not match the expected image in a pixel-perfect manner.

        Similar to `to_be`, this method initiates by comparing the metadata of both images. If a discrepancy
        in height or width is found, the assertion is immediately considered successful without further analysis.
        Conversely, if the metadata are identical, it proceeds with a pixel-by-pixel comparison to confirm that
        at least one pixel differs between the actual and expected images.

        Args:
            expected_value (Image): The expected image that should not match the actual image.

        Returns:
            ImageExpectationResult: An object containing the result of the comparison, indicating whether the
                                    actual image is indeed different from the expected image and including any
                                    pertinent comparison details.
        """
        comparison_info = self._compare(expected_value, 0)
        return ImageExpectationResult(
            actual_value=self.actual_value,
            expected_value=expected_value,
            processing_data=comparison_info,
            method="not_to_be",
            result=not comparison_info.get("result", False),
        )

    def to_be_similar(
        self, expected_value: Image, mismatch_threshold: int
    ) -> ImageExpectationResult:
        """
        Asserts that the actual image is similar to the expected image, considering a specified mismatch threshold.

        This method allows for a more flexible comparison than pixel-perfect methods. If `mismatch_threshold` is zero,
        the comparison is pixel-perfect. For values greater than zero, the images can differ up to the specified threshold
        of mismatch percentage. During the comparison, the images may be resized to common dimensions to accurately assess
        their similarity. The similarity is quantified as a match score, which reflects the percentage of similarity between
        the images.

        If the match score does not reach 100% (implying perfect similarity), a difference image object is generated to
        visualize the discrepancies. The comparison considers the images to be similar if the match score is above the
        threshold defined by 100% minus the mismatch threshold.

        Args:
            expected_value (Image): The expected image to compare against the actual image.
            mismatch_threshold (int): The acceptable percentage of mismatch between the images,
                                      with 0 indicating a pixel-perfect comparison.

        Returns:
            ImageExpectationResult: An object containing the result of the comparison, the match score, and
                                    potentially a difference image object if the match is not perfect. The result
                                    indicates whether the actual image is considered similar to the expected image
                                    within the defined tolerance.
        """
        comparison_info = self._compare(expected_value, mismatch_threshold)
        human_readable_description = "Image similarity"
        return ImageExpectationResult(
            actual_value=self.actual_value,
            expected_value=expected_value,
            processing_data=comparison_info,
            method="to_be_similar",
            human_readable_description=human_readable_description,
            result=comparison_info.get("result", False),
        )

    def _compare(self, expected_value: Image, mismatch_threshold: float = 10.0):
        """
        Compares the actual image with an expected image, considering the mismatch threshold.

        Args:
            expected_value (Image): The image to compare against the actual image.
            mismatch_threshold (float): The maximum allowed mismatch percentage between the images.

        Returns:
            dict: A dictionary containing the comparison result, match score, and additional details.
        """
        pixel_perfect = mismatch_threshold == 0
        self._make_image_diff_object(expected_value, pixel_perfect)

        comparison_info = self._make_comparison_info(
            mismatch_threshold, expected_value, pixel_perfect
        )
        self._cleanup()
        return comparison_info

    def _make_comparison_info(
        self, mismatch_threshold: float, expected_value: Image, pixel_perfect: bool
    ):
        """
        Creates a dictionary containing detailed information about the image comparison process and its results.

        This method synthesizes the comparison data, capturing key metrics and states relevant to understanding how the
        actual and expected images were evaluated against each other. The dictionary includes the overall result (a boolean
        indicating if the images are considered similar within the defined threshold), the comparison type (proportional or
        scaled based on the pixel_perfect flag), actual and expected image dimensions, aspect ratio, a detailed match score,
        and a difference image if applicable.

        The match score quantifies the degree of similarity between the images, and the presence of a difference image offers
        a visual representation of where and how the images differ. The method also considers if the images are proportional,
        which affects the comparison logic when not performing a pixel-perfect analysis.

        Args:
            mismatch_threshold (float): The maximum allowed mismatch percentage between the images for a non-pixel-perfect comparison.
            expected_value (Image): The expected image being compared against.
            pixel_perfect (bool): Flag indicating whether the comparison should be pixel-perfect.

        Returns:
            dict: A dictionary containing detailed results of the image comparison, including success status,
                  comparison metrics, and visual aids for analysis.
        """
        match_score = self._calculate_match_score()
        result = match_score >= (100 - mismatch_threshold)
        return {
            "result": result,
            "proportional": self._are_images_proportional(expected_value),
            "scaled": not pixel_perfect
            and not self._are_images_proportional(expected_value),
            "actual_value_width": self.actual_value.width,
            "actual_value_height": self.actual_value.height,
            "ratio": self.actual_value.aspect_ratio,
            "difference_image": self._generate_difference_image(),
            "match_score": match_score,
        }

    def _calculate_match_score(self):
        """
        Calculates a match score reflecting the similarity between the actual and expected images.

        This method computes the match score based on the pixel differences between the actual and
        expected images. The score is a percentage value where 100% represents a perfect match (no differences),
        and lower values indicate greater disparities. The calculation involves analyzing the pixel intensity
        differences across the images and transforming this data into a comprehensible score.

        The method does not require any input parameters because it operates on the internal state maintained
        by the class, specifically using the _image_difference attribute which should be previously populated
        through the comparison process.

        Returns:
            float: The calculated match score, ranging from 0 to 100, where 100 signifies an exact match and
                   lower values represent less similarity.
        """
        score = 100 - (np.mean(self._image_difference) * 100) / 255

        return score

    def _make_image_diff_object(self, expected_value: Image, pixel_perfect: bool):
        """
        Generates a difference object representing the pixel-wise discrepancies between the actual and expected images.

        This method prepares the actual and expected images for a detailed comparison, adjusting their sizes if necessary
        to ensure they can be compared on a pixel-by-pixel basis. In the context of a pixel-perfect comparison, the images
        are compared directly without any alterations. However, for non-pixel-perfect comparisons, the method resizes the
        expected image to match the dimensions of the actual image while maintaining the aspect ratio, facilitating an
        accurate and fair comparison.

        The resulting difference object is a numerical array where each value represents the absolute difference between
        the corresponding pixels in the actual and expected images. This object is essential for subsequent analysis and
        visualization of the image differences.

        Args:
            expected_value (Image): The expected image to compare against the actual image.
            pixel_perfect (bool): Indicates whether the comparison should be pixel-perfect. If False, the expected image
                                  will be resized to match the actual image's dimensions for a proportional comparison.

        Returns:
            numpy.ndarray: An array representing the pixel-wise absolute differences between the actual and expected images.
        """
        # Resize images for comparison if not pixel-perfect.
        self._actual_working = self.actual_value.image.copy()
        self._expected_working = expected_value.image.copy()

        if not pixel_perfect:
            scale = min(
                self._actual_working.shape[1] / self._expected_working.shape[1],
                self._actual_working.shape[0] / self._expected_working.shape[0],
            )
            self._expected_working = cv2.resize(
                self._expected_working,
                None,
                fx=scale,
                fy=scale,
                interpolation=cv2.INTER_AREA,
            )

        # Calculate difference and match score.
        self._image_difference = cv2.absdiff(
            self._actual_working, self._expected_working
        )
        return self._image_difference

    def _generate_difference_image(self):
        """
        Creates a visual representation of the differences between the actual and expected images.

        This method generates a difference image that illustrates the disparities identified during the comparison.
        Different colors are used to represent various types of differences: red for actual differences, green for
        expected differences, and purple for color discrepancies. This visualization aids in the intuitive understanding
        of where and how the images diverge.

        The method enhances the interpretability of the comparison by including a legend within the generated image,
        explaining what each color represents. The resulting image is particularly useful for detailed analysis and
        reporting purposes, providing a clear and immediate visual account of the comparison results.

        No input parameters are required as the method operates on the internal state of the class, specifically utilizing
        the _image_difference array previously established during the image comparison process.

        Returns:
            str: A base64-encoded string representing the difference image with an appended legend, suitable for
                 embedding in HTML or other display mediums.
        """
        diff_image = self._generate_base_difference_image()

        diff_image = _generate_diff_image_with_legend(diff_image)

        # Convert to base64 for consistency
        _, buffer = cv2.imencode(".png", diff_image)
        base64_image = base64.b64encode(buffer).decode("utf-8")

        return f"data:image/png;base64,{base64_image}"

    def _cleanup(self):
        self._actual_working = None
        self._expected_working = None
        self._image_difference = None

    def _generate_base_difference_image(self):
        """
        Generates a base difference image that visually represents the primary differences between the actual and expected images.

        This method creates an initial difference image by calculating and visualizing the absolute differences between the
        actual and expected images at a pixel level. The result is a grayscale image where the intensity of each pixel
        corresponds to the difference magnitude at that location. Subsequent processing can apply color codes to this base
        image to denote different types of discrepancies (e.g., actual mismatches, expected variances, color differences).

        The base difference image is crucial for detailed analysis, allowing users to identify the regions with discrepancies
        quickly. It forms the groundwork upon which further interpretative layers (like legends and color coding) are added
        to enhance understanding and communication of the comparison results.

        No input parameters are required, as the method utilizes the internally stored image difference data produced during
        the comparison process.

        Returns:
            numpy.ndarray: An array representing the grayscale base difference image, highlighting areas where the actual
                           and expected images do not align.
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
        diff_image[actual_mask_diff] = RED  # Red for actual differences
        diff_image[expected_mask_diff] = GREEN  # Green for expected differences
        diff_image[color_mask_diff] = PURPLE  # Bright purple for color differences

        return diff_image

    def _are_images_proportional(self, expected_value: Image):
        """
        Determines whether the actual and expected images have proportional dimensions, based on their aspect ratios.

        This method compares the aspect ratios of the actual and expected images to check if they are the same,
        indicating that the images are proportional. Proportionality is a significant factor in image comparisons,
        especially when resizing images for non-pixel-perfect comparisons. Ensuring that images are proportional
        allows for more accurate and meaningful comparisons, as it maintains the integrity of the visual content
        during scaling operations.

        Args:
            expected_value (Image): The expected image being compared against the actual image.

        Returns:
            bool: True if the actual and expected images have the same aspect ratio and are therefore proportional,
                  False otherwise.
        """
        return self.actual_value.aspect_ratio == expected_value.aspect_ratio
