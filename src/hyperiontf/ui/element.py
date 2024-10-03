import time
from typing import Optional, Union, List, Type

from hyperiontf.logging import getLogger
from hyperiontf.typing import NoSuchElementException
from hyperiontf.ui.decorators.element_error_recovery import error_recovery

from .locatable import LocatableElement
from hyperiontf.assertions.expectation_result import ExpectationResult
from hyperiontf.helpers.decorators.wait import wait
from hyperiontf.helpers.rect_helpers import are_rectangles_equal
from hyperiontf.image_processing.image import Image
from hyperiontf.ui.helpers.prepare_expect_object import prepare_expect_object

from hyperiontf.configuration import config
from hyperiontf.typing import VisualModeType
from hyperiontf.assertions.image_expectation_result import ImageExpectationResult

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

logger = getLogger("Element")


class Element(LocatableElement):
    def __init__(self, parent, locator, name):
        super().__init__(parent, locator, name)
        self._wait_previous_elements_rect: Optional[dict] = None

    def __resolve_eql_chain__(self, chain):
        if not self.__is_present__():
            return None

        if len(chain) > 1:
            raise Exception("Element cant have child elements!")

        if chain[0].get("attr_type", None) == "style":
            return self.get_style(chain[0]["name"])
        elif chain[0]["name"] == "text":
            return self.get_text()
        else:
            return self.get_attribute(chain[0]["name"])

    def __is_present__(self):
        """
        Checks if the element is currently present in the DOM.

        Returns:
            bool: True if the element is present, False otherwise.
        """
        if isinstance(self.element_adapter, NoSuchElementException):
            return False

        # edge case for Playwright, when by some reason exception is not risen ,the adapter instance is created with an
        # empty element
        if self.element_adapter.element is None:
            return False

        return True

    @property
    def location(self):
        return self.get_location()

    @property
    def size(self):
        return self.get_size()

    @property
    def rect(self):
        return self.get_rect()

    @property
    def is_present(self):
        return self.__is_present__()

    def __is_interactive__(self):
        """
        Checks if the element is interactive, meaning it is present and can be interacted with.

        Raises:
            NoSuchElementException: If the element is not present.
        """
        if not self.__is_present__():
            raise self.element_adapter
        # TODO: add extra interactivity verifications

    @error_recovery(logger=logger)
    def send_keys(self, data: Union[str, List[str]]):
        """
        Sends input data to the element.

        Parameters:
            data (Union[str, List[str]]): The data to be sent to the element.
        """
        logger.info(f"[{self.__full_name__}] sending input data:\n{data}")
        self.element_adapter.send_keys(data)

    fill = send_keys

    @error_recovery(logger=logger)
    def clear(self):
        """
        Clears the input field of the element.
        """
        logger.info(f"[{self.__full_name__}] clearing input")
        self.element_adapter.clear()

    @error_recovery(logger=logger)
    def clear_and_fill(self, data: Union[str, List[str]]):
        """
        Clears the input field and then sends new input data to the element.

        Parameters:
            data (Union[str, List[str]]): The new data to be sent to the element.
        """
        logger.info(
            f"[{self.__full_name__}] clearing input and sending new input data:\n{data}"
        )
        self.element_adapter.clear()
        self.element_adapter.send_keys(data)

    @error_recovery(logger=logger)
    def click(self):
        """
        Clicks on the element.
        """
        logger.info(f"[{self.__full_name__}] click")
        self.element_adapter.click()

    @error_recovery(logger=logger)
    def submit(self):
        """
        Submits the form that the element belongs to.
        """
        logger.info(f"[{self.__full_name__}] submit")
        self.element_adapter.submit()

    @error_recovery(logger=logger)
    def get_text(self, log: bool = True) -> str:
        """
        Retrieves the text content of the element.

        Parameters:
            log (bool): If True, logs the retrieved text.

        Returns:
            str: The text content of the element.
        """
        text = self.element_adapter.text.strip()
        if log:
            logger.info(f"[{self.__full_name__}] getting element's text:\n{text}")
        return text

    @error_recovery(logger=logger)
    def get_attribute(self, attr_name: str, log: bool = True) -> str:
        """
        Retrieves the value of a specified attribute of the element.

        Parameters:
            attr_name (str): The name of the attribute to retrieve.
            log (bool): If True, logs the retrieved attribute value.

        Returns:
            str: The value of the specified attribute.
        """
        text = self.element_adapter.attribute(attr_name).strip()
        if log:
            logger.info(
                f"[{self.__full_name__}] getting element's '{attr_name}' attribute value:\n{text}"
            )
        return text

    @error_recovery(logger=logger)
    def get_style(self, attr_name: str, log: bool = True) -> str:
        """
        Retrieves the value of a specified CSS style property of the element.

        Parameters:
            attr_name (str): The name of the style property to retrieve.
            log (bool): If True, logs the retrieved style property value.

        Returns:
            str: The value of the specified style property.
        """
        text = self.element_adapter.style(attr_name)
        if log:
            logger.info(
                f"[{self.__full_name__}] getting element's '{attr_name}' style property value:\n{text}"
            )
        return text

    @error_recovery(logger=logger)
    def _get_is_enabled(self, log: bool = True) -> bool:
        """
        Checks if the element is enabled, indicating that it can be interacted with.

        Parameters:
            log (bool): If True, logs the enabled state of the element.

        Returns:
            bool: True if the element is enabled, False otherwise.
        """
        is_enabled = self.element_adapter.is_enabled
        if log:
            logger.info(
                f"[{self.__full_name__}] getting element's 'enabled' attribute: {is_enabled}"
            )
        return is_enabled

    @error_recovery(logger=logger)
    def _get_is_displayed(self, log: bool = True) -> bool:
        """
        Checks if the element is displayed on the page.

        Parameters:
            log (bool): If True, logs the displayed state of the element.

        Returns:
            bool: True if the element is visible on the page, False otherwise.
        """
        is_displayed = self.element_adapter.is_displayed
        if log:
            logger.info(
                f"[{self.__full_name__}] getting element's 'displayed' attribute: {is_displayed}"
            )
        return is_displayed

    @error_recovery(logger=logger)
    def _get_is_selected(self, log: bool = True) -> bool:
        """
        Checks if the element is selected (e.g., checkboxes, radio buttons).

        Parameters:
            log (bool): If True, logs the selected state of the element.

        Returns:
            bool: True if the element is selected, False otherwise.
        """
        is_selected = self.element_adapter.is_selected
        if log:
            logger.info(
                f"[{self.__full_name__}] getting element's 'selected' attribute: {is_selected}"
            )
        return is_selected

    @property
    def is_enabled(self) -> bool:
        """
        A property to check if the element is enabled.

        Returns:
            bool: True if the element is enabled, False otherwise.
        """
        return self._get_is_enabled()

    @property
    def is_hidden(self) -> bool:
        """
        A property to check if the element is hidden (not displayed).

        Returns:
            bool: True if the element is not displayed, False otherwise.
        """
        return not self._get_is_displayed()

    @property
    def is_visible(self) -> bool:
        """
        A property to check if the element is visible on the page.

        Returns:
            bool: True if the element is displayed, False otherwise.
        """
        return self._get_is_displayed()

    @property
    def is_disabled(self) -> bool:
        """
        A property to check if the element is disabled.

        Returns:
            bool: True if the element is not enabled, False otherwise.
        """
        return not self._get_is_enabled()

    @property
    def is_selected(self) -> bool:
        """
        A property to check if the element (e.g., a checkbox or radio button) is selected.

        Returns:
            bool: True if the element is selected, False otherwise.
        """
        return self._get_is_selected()

    @error_recovery(logger=logger)
    def get_location(self, log: bool = True) -> dict:
        """
        Retrieves the location of the element in the page.

        Parameters:
            log (bool): If True, logs the location of the element.

        Returns:
            dict: The X and Y coordinates of the element.
        """
        location = self.element_adapter.location
        if log:
            logger.info(
                f"[{self.__full_name__}] getting element's location: {location}"
            )
        return location

    @error_recovery(logger=logger)
    def get_size(self, log: bool = True) -> dict:
        """
        Retrieves the size of the element.

        Parameters:
            log (bool): If True, logs the size of the element.

        Returns:
            dict: The width and height of the element.
        """
        size = self.element_adapter.size
        if log:
            logger.info(f"[{self.__full_name__}] getting element's size: {size}")
        return size

    def _prepare_action_builder(self):
        builder = self.root.action_builder
        builder.sender = self.__full_name__
        builder.logger = logger
        return builder

    @error_recovery(logger=logger)
    def get_rect(self, log: bool = True) -> dict:
        """
        Retrieves the rectangle that bounds the element, including its location and size.

        Parameters:
            log (bool): If True, logs the rectangle details of the element.

        Returns:
            dict: A dictionary containing the location and size of the element.
        """
        rect = self.element_adapter.rect
        if log:
            logger.info(
                f"[{self.__full_name__}] getting element's rectangle(location + size): {rect}"
            )
        return rect

    @error_recovery(logger=logger)
    def make_screenshot(self, filepath: Optional[str] = None) -> Image:
        """
        Takes a screenshot of the element.

        Parameters:
            filepath (Optional[str]): The file path where the screenshot should be saved. If not specified,
                                      the screenshot will be returned as a base64 encoded string.

        Returns:
            Union[str, None]: The base64 encoded string of the screenshot if no filepath is provided, otherwise None.
        """
        return Image(path=filepath, img_data=self.element_adapter.screenshot_as_base64)

    def screenshot(
        self,
        message: Optional[str] = "Element screen snap",
        title: Optional[str] = "Element screen snap",
    ):
        """
        Logs a screenshot of the element along with a custom message and title.

        Parameters:
            message (Optional[str]): The message to accompany the screenshot in the log.
            title (Optional[str]): The title for the screenshot attachment in the log.
        """
        logger.info(
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

    def assert_text(self, expected_text) -> Type[ExpectationResult]:
        """
        Asserts that the element's text matches the expected text. This method simplifies the syntax
        by directly integrating the assertion with the element's text retrieval, reducing code verbosity
        and enhancing readability and supportability.

        Behind the scenes, this utilizes the Expect class to perform the comparison and logging,
        ensuring that an exception is raised if the assertion fails, providing immediate feedback
        on test failure with detailed traceability.

        Parameters:
            expected_text (str): The text that the element's text should match.

        Returns:
            ExpectationResult: An object representing the result of the comparison, which also behaves
                                as a boolean indicating the success (True) or failure (False) of the assertion.

        Raises:
            FailedExpectationException: If the actual text of the element does not match the expected text.
        """
        actual_value = self.get_text(log=False)
        expect = prepare_expect_object(
            self, actual_value, True, "Asserting element's text.", logger
        )
        return expect.to_be(expected_text)

    def assert_attribute(self, attr_name, expected_text) -> Type[ExpectationResult]:
        """
        Asserts that a specific attribute of the element has the expected value. Similar to `assert_text`,
        this method leverages the framework's assertion API to minimize verbosity by combining attribute retrieval
        and assertion into a single operation.

        It uses the Expect class for performing the comparison, logging the result, and raising an exception
        if the assertion fails, thus halting the test execution for immediate issue identification.

        Parameters:
            attr_name (str): The name of the attribute to assert against.
            expected_text (str): The expected value of the attribute.

        Returns:
            ExpectationResult: The outcome of the assertion, acting as a boolean value to indicate success or failure.

        Raises:
            FailedExpectationException: If the actual value of the specified attribute does not match the expected value.
        """
        actual_value = self.get_attribute(attr_name, log=False)
        expect = prepare_expect_object(
            self,
            actual_value,
            True,
            f"Asserting element's '{attr_name}' attribute",
            logger,
        )
        return expect.to_be(expected_text)

    def assert_style(self, attr_name, expected_text) -> Type[ExpectationResult]:
        """
        Asserts that the element's style for a given property matches the expected value. This convenience method
        reduces code complexity by encapsulating both the retrieval of the style property and the assertion logic
        into one straightforward call.

        Utilizing the Expect class, this method ensures detailed logging and comparison, throwing an exception
        for a failed assertion to provide clear feedback during test execution.

        Parameters:
            attr_name (str): The CSS style property to check.
            expected_text (str): The expected value of the style property.

        Returns:
            ExpectationResult: A boolean-like object indicating the assertion result, with detailed comparison logs.

        Raises:
            FailedExpectationException: If the element's style value does not meet the expected condition.
        """
        actual_value = self.get_style(attr_name, log=False)
        expect = prepare_expect_object(
            self,
            actual_value,
            True,
            f"Asserting element's '{attr_name}' style value.",
            logger,
        )
        return expect.to_be(expected_text)

    def verify_text(self, expected_text) -> Type[ExpectationResult]:
        """
        Verifies that the element's text matches the expected text without stopping test execution on failure.
        This method provides a non-blocking approach to check element states, logging all outcomes for traceability.

        Utilizing the Expect class for comparison, it logs the result extensively, allowing the test to continue
        even if the verification fails, thus enhancing issue traceability while maintaining test flow.

        Parameters:
            expected_text (str): The text that the element's text is expected to match.

        Returns:
            ExpectationResult: An object representing the verification result, behaving as a boolean to indicate
                                success (True) or failure (False), with detailed logging for both outcomes.
        """
        actual_value = self.get_text(log=False)
        verify = prepare_expect_object(
            self, actual_value, False, "Verifying element's text.", logger
        )
        return verify.to_be(expected_text)

    def verify_attribute(self, attr_name, expected_text) -> Type[ExpectationResult]:
        """
        Verifies the value of a specific attribute of the element matches the expected value, logging the outcome
        without halting the test on failure. This method simplifies checking attribute values by combining retrieval
        and verification, providing clear logs for both success and failure cases.

        It leverages the Expect class for detailed comparison and logging, enhancing test traceability without
        interrupting the test flow for verifications.

        Parameters:
            attr_name (str): The name of the attribute to verify.
            expected_text (str): The expected attribute value.

        Returns:
            ExpectationResult: A boolean-like object indicating the verification result, with comprehensive logs.

        """
        actual_value = self.get_attribute(attr_name, log=False)
        verify = prepare_expect_object(
            self,
            actual_value,
            False,
            f"Verifying element's '{attr_name}' attribute",
            logger,
        )
        return verify.to_be(expected_text)

    def verify_style(self, attr_name, expected_text) -> Type[ExpectationResult]:
        """
        Verifies the element's style for a given property matches the expected value, providing extensive logging
        for both success and failure without stopping the test. This method reduces verbosity by encapsulating the
        style property retrieval and verification in one call, improving readability and maintainability.

        Uses the Expect class for comparison, ensuring that detailed outcome logs are produced, thereby facilitating
        better issue traceability while allowing test execution to continue regardless of the verification result.

        Parameters:
            attr_name (str): The CSS style property to verify.
            expected_text (str): The expected value for the style property.

        Returns:
            ExpectationResult: An object representing the verification outcome, acting as a boolean for success or
                                failure, with detailed logging included.

        """
        actual_value = self.get_style(attr_name, log=False)
        verify = prepare_expect_object(
            self,
            actual_value,
            False,
            f"Verifying element's '{attr_name}' style value.",
            logger,
        )
        return verify.to_be(expected_text)

    def assert_visible(self) -> Type[ExpectationResult]:
        """
        Asserts that the element is visible on the page. It utilizes a private method to check visibility
        without additional logging, integrating seamlessly with the framework's assertion API for clarity
        and succinctness in test scripts.

        This method leverages the Expect class for performing the assertion and logging, raising an exception
        if the assertion fails, to provide immediate feedback on test failure with detailed traceability.

        Returns:
            ExpectationResult: An object representing the assertion result, behaving as a boolean to indicate
                                the success (True) or failure (False) of the assertion.

        Raises:
            AssertionError: If the element is not visible.
        """
        actual_value = self._get_is_displayed(log=False)
        expect = prepare_expect_object(
            self, actual_value, True, "Asserting element's visibility.", logger
        )
        return expect.to_be(True)

    def verify_visible(self) -> Type[ExpectationResult]:
        """
        Verifies that the element is visible on the page without stopping test execution on failure.
        This method enhances script readability and test flow by providing a non-blocking verification
        with detailed outcome logging.

        Returns:
            ExpectationResult: An object representing the verification result, acting as a boolean to indicate
                                success (True) or failure (False), with detailed logging for both outcomes.
        """
        actual_value = self._get_is_displayed(log=False)
        verify = prepare_expect_object(
            self, actual_value, False, "Verifying element's visibility.", logger
        )
        return verify.to_be(True)

    def assert_hidden(self) -> Type[ExpectationResult]:
        """
        Asserts that the element is hidden (not displayed) on the page. This method uses a private method
        to check the element's hidden state without additional logging, ensuring test script clarity and
        maintenance ease.

        Returns:
            ExpectationResult: An object indicating the assertion result, capable of acting as a boolean value.
                                Detailed logging is provided for traceability.

        Raises:
            AssertionError: If the element is visible instead of hidden.
        """
        actual_value = self._get_is_displayed(log=False)
        expect = prepare_expect_object(
            self, actual_value, True, "Asserting element's hidden state.", logger
        )
        return expect.to_be(False)

    def verify_hidden(self) -> Type[ExpectationResult]:
        """
        Verifies that the element is hidden (not displayed) on the page, providing a flexible verification
        method that logs outcomes without interrupting test execution on failure.

        Returns:
            ExpectationResult: A boolean-like object indicating the verification outcome, with extensive logging
                                provided for both success and failure cases.
        """
        actual_value = self._get_is_displayed(log=False)
        verify = prepare_expect_object(
            self, actual_value, False, "Verifying element's hidden state.", logger
        )
        return verify.to_be(False)

    def assert_enabled(self) -> Type[ExpectationResult]:
        """
        Asserts that the element is enabled and interactive. It utilizes a private method to check the
        enabled state without additional logging, streamlining integration with the framework's assertion API.

        This method leverages the Expect class for performing the assertion and logging, raising an exception
        if the assertion fails, to provide immediate feedback on test failure with detailed traceability.

        Returns:
            ExpectationResult: An object representing the assertion result, behaving as a boolean to indicate
                                the success (True) or failure (False) of the assertion.

        Raises:
            AssertionError: If the element is not enabled.
        """
        actual_value = self._get_is_enabled(log=False)
        expect = prepare_expect_object(
            self, actual_value, True, "Asserting element's enabled state.", logger
        )
        return expect.to_be(True)

    def verify_enabled(self) -> Type[ExpectationResult]:
        """
        Verifies that the element is enabled without stopping test execution on failure. This method provides
        a non-blocking approach to check the element's enabled state, enhancing test flow with detailed logging.

        Returns:
            ExpectationResult: An object representing the verification result, acting as a boolean to indicate
                                success (True) or failure (False), with detailed logging for both outcomes.
        """
        actual_value = self._get_is_enabled(log=False)
        verify = prepare_expect_object(
            self, actual_value, False, "Verifying element's enabled state.", logger
        )
        return verify.to_be(True)

    def assert_disabled(self) -> Type[ExpectationResult]:
        """
        Asserts that the element is disabled. This method uses a private method to check the element's disabled
        state without additional logging, ensuring clarity and ease of maintenance in test scripts.

        Returns:
            ExpectationResult: An object indicating the assertion result, capable of acting as a boolean value.
                                Detailed logging is provided for traceability.

        Raises:
            AssertionError: If the element is enabled instead of disabled.
        """
        actual_value = self._get_is_enabled(log=False)
        expect = prepare_expect_object(
            self, actual_value, True, "Asserting element's disabled state.", logger
        )
        return expect.to_be(False)

    def verify_disabled(self) -> Type[ExpectationResult]:
        """
        Verifies that the element is disabled, logging the outcome without interrupting test execution on failure.
        This method offers a flexible verification approach with comprehensive outcome logging for better traceability.

        Returns:
            ExpectationResult: A boolean-like object indicating the verification outcome, with extensive logging
                                provided for both success and failure cases.
        """
        actual_value = self._get_is_enabled(log=False)
        verify = prepare_expect_object(
            self, actual_value, False, "Verifying element's disabled state.", logger
        )
        return verify.to_be(False)

    def assert_selected(self) -> Type[ExpectationResult]:
        """
        Asserts that the element is selected (e.g., for checkboxes or radio buttons). It uses a private method
        to check the selected state without additional logging, integrating seamlessly with the framework's
        assertion API for clear and concise test scripts.

        This method employs the Expect class to perform the assertion and logging, raising an exception if
        the assertion fails, to provide immediate feedback on test failure with detailed traceability.

        Returns:
            ExpectationResult: An object representing the assertion result, behaving as a boolean to indicate
                                the success (True) or failure (False) of the assertion.

        Raises:
            AssertionError: If the element is not selected.
        """
        actual_value = self._get_is_selected(log=False)
        expect = prepare_expect_object(
            self, actual_value, True, "Asserting element's selected state.", logger
        )
        return expect.to_be(True)

    def verify_selected(self) -> Type[ExpectationResult]:
        """
        Verifies that the element is selected without stopping test execution on failure. This method offers
        a non-blocking approach to verify the element's selected state, enhancing test flow with detailed logging.

        Returns:
            ExpectationResult: An object representing the verification result, acting as a boolean to indicate
                                success (True) or failure (False), with detailed logging for both outcomes.
        """
        actual_value = self._get_is_selected(log=False)
        verify = prepare_expect_object(
            self, actual_value, False, "Verifying element's selected state.", logger
        )
        return verify.to_be(True)

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
            logger,
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
            logger,
        )

    def verify_visual_match_in_regions(
        self,
        expected_value: Union[Image, str],
        compare_regions: Optional[list] = None,
        mismatch_threshold: float = config.visual.default_partial_mismatch_threshold,
        mode: VisualModeType = config.visual.mode,
    ):

        return verify_visual_match_in_regions(
            self, expected_value, compare_regions, mismatch_threshold, mode, logger
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
            self, expected_value, compare_regions, mismatch_threshold, mode, logger
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
            self, expected_value, exclude_regions, mismatch_threshold, mode, logger
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
            self, expected_value, exclude_regions, mismatch_threshold, mode, logger
        )

    @wait()
    def wait_until_found(self):
        """
        Waits until the element is found on the page. This method continuously attempts to find the element until it is present or the specified timeout is reached.

        Parameters:
        - timeout (float, optional): The maximum time in seconds to wait for the element to be found. If not specified, a default timeout value is used.
        - raise_exception (bool, optional): If set to True, an exception will be raised if the element is not found within the timeout period. If False or not specified, no exception will be raised, and the method will return False if the element is not found.

        Returns:
            bool: True if the element is found within the timeout, False otherwise.

        Note:
            This method utilizes a retry mechanism with a sleep interval between attempts to find the element. The behavior regarding timeouts and exception handling can be customized by the `timeout` and `raise_exception` parameters.
        """
        if not self.__is_present__():
            return self._wait_false_hook()

        return True

    @wait()
    def wait_until_missing(self):
        """
        Waits until the element is no longer present on the page or in the DOM. This method continuously checks for the element's presence until it is confirmed to be missing or the specified timeout is reached.

        Parameters:
        - timeout (float, optional): The maximum time in seconds to wait for the element to be confirmed as missing. If not specified, a default timeout value is used.
        - raise_exception (bool, optional): If set to True, an exception will be raised if the element is still present after the timeout period. If False or not specified, no exception will be raised, and the method will return False if the element is still found.

        Returns:
            bool: True if the element is confirmed missing within the timeout, False otherwise.

        Note:
            This method is particularly useful for scenarios where the removal of an element from the DOM is required before proceeding, such as after triggering an action that leads to the deletion of a UI component.
        """
        if self.__is_present__():
            return self._wait_false_hook()

        return True

    @wait()
    def wait_until_visible(self):
        """
        Waits until the element becomes visible on the page. This method continuously checks the element's visibility until it becomes visible or the specified timeout is reached.

        Parameters:
        - timeout (float, optional): The maximum time in seconds to wait for the element to become visible. If not specified, a default timeout value is used.
        - raise_exception (bool, optional): If set to True, an exception will be raised if the element does not become visible within the timeout period. If False or not specified, no exception will be raised, and the method will return False if the element is not visible.

        Returns:
            bool: True if the element becomes visible within the timeout, False otherwise.
        """
        if not self.__is_present__() or not self._get_is_displayed(log=False):
            return self._wait_false_hook()

        return True

    @wait()
    def wait_until_enabled(self):
        """
        Waits until the element is enabled and thus interactable. This method continuously checks the element's enabled state until it is enabled or the specified timeout is reached.

        Parameters:
        - timeout (float, optional): The maximum time in seconds to wait for the element to become enabled. If not specified, a default timeout value is used.
        - raise_exception (bool, optional): If set to True, an exception will be raised if the element does not become enabled within the timeout period. If False or not specified, no exception will be raised, and the method will return False if the element is not enabled.

        Returns:
            bool: True if the element becomes enabled within the timeout, False otherwise.
        """
        if not self.__is_present__() or not self._get_is_enabled(log=False):
            return self._wait_false_hook()

        return True

    @wait()
    def wait_until_interactable(self):
        """
        Waits until the element is in a state that allows for user interaction, such as being visible and enabled. This method continuously checks the element's state until it is deemed interactable or the specified timeout is reached.

        Parameters:
        - timeout (float, optional): The maximum time in seconds to wait for the element to become interactable. If not specified, a default timeout value is used.
        - raise_exception (bool, optional): If set to True, an exception will be raised if the element does not become interactable within the timeout period. If False or not specified, no exception will be raised, and the method will return False if the element is not interactable.

        Returns:
            bool: True if the element becomes interactable within the timeout, False otherwise.
        """
        if not self.__is_present__() or not self._is_user_interactable():
            return self._wait_false_hook()

        return True

    @wait()
    def wait_until_hidden(
        self,
    ):
        """
        Waits until the element is no longer visible on the page. This method continuously checks the element's visibility status until it becomes hidden or the specified timeout is reached.

        Parameters:
        - timeout (float, optional): The maximum time in seconds to wait for the element to become hidden. If not specified, a default timeout value is used.
        - raise_exception (bool, optional): If set to True, an exception will be raised if the element does not become hidden within the timeout period. If False or not specified, no exception will be raised, and the method will return False if the element remains visible.

        Returns:
            bool: True if the element becomes hidden within the timeout, False otherwise.

        Note:
            This method is useful for scenarios where the disappearance of an element from the page is required before proceeding, such as waiting for a loading indicator to vanish.
        """
        if not self.__is_present__() or self._get_is_displayed(log=False):
            return self._wait_false_hook()

        return True

    @wait()
    def wait_until_animation_completed(self):
        """
        Waits until any ongoing animation on the element is completed. The method checks the element's position and size at three different points in time, with a short delay between each check. If the position and size remain the same across these checks, the method concludes that any animation has completed.

        This method introduces an artificial delay as it requires multiple checks with delays in between to ensure the animation has finished. This is different from other wait methods, which exit immediately if their conditions are satisfied.

        Parameters:
        - timeout (float, optional): The maximum time in seconds to wait for the animation to complete. If not specified, a default timeout value is used. The timeout should account for the time taken by the checks and delays between them.
        - raise_exception (bool, optional): If set to True, an exception will be raised if the animation does not complete within the timeout period. If False or not specified, no exception will be raised, and the method will return False if the animation is still ongoing.

        Returns:
            bool: True if the element's animation is completed within the timeout, False otherwise.

        Note:
            This method is particularly useful for ensuring that elements are stable and ready for interaction, especially after dynamic content loading or visual transitions. It ensures that actions like clicks are performed on elements only after they have become fully interactive.
        """
        if not self.__is_present__():
            return self._wait_false_hook()

        current_rect = self.get_rect(log=False)
        if self._wait_previous_elements_rect is None or not are_rectangles_equal(
            self._wait_previous_elements_rect, current_rect
        ):
            self._wait_update_rect_hook(current_rect)
            return self._wait_false_hook()

        self._wait_previous_elements_rect = None
        return True

    @wait()
    def wait_until_fully_interactable(self):
        """
        Waits until the element is fully ready for interaction. This comprehensive check includes verifying that the element is visible, has no ongoing animations, and is enabled. It ensures the element is stable and interactable, combining several verification steps into a single method to simplify automation scripts.

        The method performs checks in the following order:
        1. Visibility: Ensures the element is visible on the page.
        2. Animation: Confirms there are no ongoing animations affecting the element by checking its position and size stability over a short period.
        3. Enabled: Verifies that the element is not disabled, ensuring it can receive user interactions like clicks.

        Parameters:
        - timeout (float, optional): The maximum time in seconds to wait for the element to become fully interactable. If not specified, a default timeout value is used. This timeout encompasses all checks performed by the method.
        - raise_exception (bool, optional): If set to True, an exception will be raised if the element does not become fully interactable within the timeout period. If False or not specified, no exception will be raised, and the method will return False if the element is not ready for interaction.

        Returns:
            bool: True if the element is fully interactable within the timeout, False otherwise.

        Note:
            This method is particularly useful in complex scenarios where multiple conditions must be satisfied before proceeding with interactions. It reduces the need for multiple separate wait calls, streamlining test scripts and interaction sequences.
        """
        if not self.__is_present__():
            return self._wait_false_hook()

        current_rect = self.get_rect(log=False)
        if (
            self._wait_previous_elements_rect is None
            or not self._is_user_interactable()
            or not are_rectangles_equal(self._wait_previous_elements_rect, current_rect)
        ):
            self._wait_update_rect_hook(current_rect)
            return self._wait_false_hook()

        self._wait_previous_elements_rect = None
        return True

    def _wait_false_hook(self) -> bool:
        self.find_itself()
        return False

    def _wait_update_rect_hook(self, current_rect: dict):
        self._wait_previous_elements_rect = current_rect
        time.sleep(0.3)

    def _is_user_interactable(self) -> bool:
        return self._get_is_displayed(log=False) and self._get_is_enabled(log=False)

    def _scroll_into_view(self):
        if not self._get_is_displayed(log=False):
            self.element_adapter.location_once_scrolled_into_view

    @error_recovery(logger=logger)
    def scroll_into_view(self):
        """
        Scroll the current element into view.

        This method ensures that the element is scrolled into the visible area of the page or container.
        It is typically used when an element is not immediately visible, and interaction with it requires
        the element to be brought into the viewport.
        """
        self._scroll_into_view()

    @error_recovery(logger=logger)
    def drag_and_drop_by(self, x: float, y: float):
        """
        Drag the current element and drop it at the specified offset coordinates.

        This method simulates dragging the element by the specified x and y offsets.
        It uses the action builder to perform the drag-and-drop action.

        Parameters:
            x (float): The horizontal offset by which to drag the element.
            y (float): The vertical offset by which to drag the element.

        Returns:
            None: The action is performed and executed using the action builder.
        """
        self._scroll_into_view()
        builder = self._prepare_action_builder()
        builder.drag_element_by(self, x, y).perform()

    @error_recovery(logger=logger)
    def drag_and_drop(self, other):
        """
        Drag the current element and drop it onto another element.

        This method simulates dragging the current element and dropping it on the target element.
        It uses the action builder to perform the drag-and-drop action between two elements.

        Parameters:
            other: The target element on which the current element will be dropped.

        Returns:
            None: The action is performed and executed using the action builder.
        """
        self._scroll_into_view()
        builder = self._prepare_action_builder()
        builder.drag_element_on_element(self, other).perform()

    @error_recovery(logger=logger)
    def right_click(self):
        """
        Perform a right-click action on the current element.

        This method simulates a right-click (context click) on the current element.
        It uses the action builder to execute the right-click operation on the element.

        Returns:
            None: The action is performed and executed using the action builder.
        """
        self._scroll_into_view()
        builder = self._prepare_action_builder()
        builder.right_click_on_element(self).perform()
