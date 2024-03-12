import base64

from .map_locator import convert_locator
from .map_exception import map_exception
from .assert_stale_element_reference import assert_stale_reference
from hyperiontf.ui import By
from hyperiontf.typing import (
    LocatorStrategies,
    UnsupportedLocatorException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By as SeleniumBy

SPECIAL_ATTRS = ["value"]


class Element:
    """
    Wrapper class for a Selenium WebElement to ensure a consistent API and remap possible exceptions
    to Hyperion exceptions for better error handling and recovery in Hyperion's algorithms.

    Args:
        element (WebElement): The Selenium WebElement to be wrapped.
        page (Page | Driver): The Page object or Driver representing the current page.
    """

    def __init__(self, element, page):
        """
        Initialize the Element object with the provided Selenium WebElement.

        Args:
            element (WebElement): The Selenium WebElement to be wrapped.
            page (Page | Driver): The Page object or Driver representing the current page.
        """
        self.element = element
        self.page = page

    @property
    @map_exception
    @assert_stale_reference
    def text(self):
        """
        Get the visible text of the element.

        Returns:
            str: The visible text of the element.

        Raises:
            HyperionException: If an error occurs while retrieving the text.

        """
        return self.element.inner_text()

    @property
    @map_exception
    @assert_stale_reference
    def is_displayed(self):
        """
        Check if the element is displayed on the page.

        Returns:
            bool: True if the element is displayed, False otherwise.

        Raises:
            HyperionException: If an error occurs while checking the display status.

        """
        return self.element.is_visible()

    @property
    @map_exception
    @assert_stale_reference
    def is_enabled(self):
        """
        Check if the element is enabled and can be interacted with.

        Returns:
            bool: True if the element is enabled and can be interacted with, False otherwise.

        Raises:
            HyperionException: If an error occurs while checking the enabled status.

        """
        return not self.element.is_disabled()

    @property
    @map_exception
    @assert_stale_reference
    def is_selected(self):
        """
        Check if the element is selected (e.g., a checkbox or radio button is checked).

        Returns:
            bool: True if the element is selected, False otherwise.

        Raises:
            HyperionException: If an error occurs while checking the selected status.

        """
        return self.element.is_checked()

    @property
    @map_exception
    @assert_stale_reference
    def size(self):
        """
        Get the size of the element.

        Returns:
            dict: A dictionary containing the width and height of the element as key-value pairs.

        Example:
            {'width': 100, 'height': 50}

        Raises:
            HyperionException: If an error occurs while getting the size of the element.

        """
        bbox = self.element.bounding_box()
        return {"width": bbox["width"], "height": bbox["height"]}

    @property
    @map_exception
    @assert_stale_reference
    def location(self):
        """
        Get the location of the element.

        Returns:
            dict: A dictionary containing the x and y coordinates of the element as key-value pairs.

        Example:
            {'x': 100, 'y': 50}

        Raises:
            HyperionException: If an error occurs while getting the location of the element.

        """
        bbox = self.element.bounding_box()
        return {"x": bbox["x"], "y": bbox["y"]}

    @property
    @map_exception
    @assert_stale_reference
    def location_once_scrolled_into_view(self):
        """
        Get the location of the element once it has been scrolled into view.

        Returns:
            dict: A dictionary containing the x and y coordinates of the element as key-value pairs.

        Example:
            {'x': 100, 'y': 50}

        Raises:
            HyperionException: If an error occurs while getting the location of the element once scrolled into view.

        """
        self.element.scroll_into_view()
        bbox = self.element.bounding_box()
        return {"x": bbox["x"], "y": bbox["y"]}

    @property
    @map_exception
    @assert_stale_reference
    def rect(self):
        """
        Get the size and location of the element.

        Returns:
            dict: A dictionary containing the x, y coordinates of the top-left corner,
            width, and height of the element as key-value pairs.

        Example:
            {'x': 100, 'y': 50, 'width': 200, 'height': 100}

        Raises:
            HyperionException: If an error occurs while getting the size and location of the element.

        """
        bbox = self.element.bounding_box()
        return {
            "x": bbox["x"],
            "y": bbox["y"],
            "width": bbox["width"],
            "height": bbox["height"],
        }

    @map_exception
    @assert_stale_reference
    def find_element(self, locator: By):
        """
        Find a single child element within the current element, based on the provided locator.

        Args:
            locator (By): The locator object representing the method to find the child element.

        Returns:
            Element: An Element object representing the found child element.

        Raises:
            HyperionException: If any exception occurs during the search for the child element.
        """
        playwright_locator = convert_locator(locator)
        if playwright_locator == LocatorStrategies.UNSUPPORTED:
            raise UnsupportedLocatorException(
                f"Unsupported {locator.by} locator for Playwright"
            )
        founded_element = self.element.query_selector(playwright_locator)
        if founded_element is None:
            raise NoSuchElementException(
                f"Element was not found!\n{playwright_locator}"
            )
        return Element(self.element.query_selector(playwright_locator), self)

    @map_exception
    @assert_stale_reference
    def find_elements(self, locator):
        """
        Find multiple child elements within the current element, based on the provided locator.

        Args:
            locator (By): The locator object representing the method to find the child elements.

        Returns:
            List[Element]: A list of Element objects representing the found child elements.

        Raises:
            HyperionException: If any exception occurs during the search for the child elements.
        """
        playwright_locator = convert_locator(locator)
        if playwright_locator == LocatorStrategies.UNSUPPORTED:
            raise UnsupportedLocatorException(
                f"Unsupported {locator.by} locator for Playwright"
            )

        elements = self.element.query_selector_all(playwright_locator)
        return list(map(lambda x: Element(x, self), elements))

    @map_exception
    @assert_stale_reference
    def send_keys(self, data):
        """
        Simulate typing the specified data into the element.

        Args:
            data (str): The text to be typed into the element.

        Raises:
            HyperionException: If any exception occurs during sending the keys.
        """
        self.element.type(data)

    @map_exception
    @assert_stale_reference
    def click(self):
        """
        Perform a click action on the element.

        Raises:
            HyperionException: If any exception occurs during the click action.
        """
        self.element.click()

    @map_exception
    @assert_stale_reference
    def attribute(self, name):
        """
        Get the value of the specified attribute of the element.

        Args:
            name (str): The name of the attribute.

        Returns:
            str: The value of the attribute.

        Raises:
            HyperionException: If any exception occurs during fetching the attribute value.
        """
        if name in SPECIAL_ATTRS:
            return self._get_special_attr(name)
        return self.element.get_attribute(name)

    def _get_special_attr(self, name):
        if name == "value":
            return self.element.evaluate("element => element.value")

        return ""

    @map_exception
    @assert_stale_reference
    def style(self, name):
        """
        Get the computed value of the specified CSS property of the element.

        Args:
            name (str): The name of the CSS property.

        Returns:
            str: The computed value of the CSS property.

        Raises:
            HyperionException: If any exception occurs during fetching the CSS property value.
        """
        return self.element.evaluate(
            f"element => window.getComputedStyle(element)['{name}']"
        )

    @map_exception
    @assert_stale_reference
    def clear(self):
        """
        Clear the input value of the element (if applicable).

        Raises:
            HyperionException: If any exception occurs during clearing the input value.
        """
        self.element.fill("")

    @map_exception
    @assert_stale_reference
    def submit(self):
        """
        Submit the form associated with the element (if applicable).

        Raises:
            HyperionException: If any exception occurs during the form submission.
        """
        # Playwright does not have a direct equivalent for the submit method,
        # you might need to find the submit button or use a JavaScript call
        self.element.eval_on_selector("element => element.closest('form').submit()")

    def _find_using_undefined_locator(self, locator, is_single: bool = True):
        """
        Find a single or multiple child elements within the current element using a custom locator strategy.
        This method is used when the provided locator strategy is not supported by the Selenium library.

        Args:
            locator (By): The locator object representing the method to find the child elements.
            is_single (bool, optional): Whether to find a single element or multiple elements. Default is True.

        Returns:
            WebElement | list[WebElement]: The found child element or a list of found child elements.

        Raises:
            HyperionException: If any exception occurs during the search for the child elements.
        """
        if locator.by == LocatorStrategies.TEST_ID:
            css_locator = f"[data-testid='{locator.value}']"
            if is_single:
                return self.element.find_element(SeleniumBy.CSS_SELECTOR, css_locator)
            else:
                return self.element.find_elements(SeleniumBy.CSS_SELECTOR, css_locator)
        if locator.by == LocatorStrategies.SCRIPT:
            return self.page.execute_script(locator.value, self.element)

        raise UnsupportedLocatorException(
            f"Unsupported {locator.by} locator for Selenium WebDriver"
        )

    @assert_stale_reference
    def get_iframe_content(self):
        return self.element.content_frame()

    @property
    @map_exception
    @assert_stale_reference
    def screenshot_as_base64(self):
        screenshot_as_bytes = self.element.screenshot()
        return base64.b64encode(screenshot_as_bytes).decode("utf-8")

    @map_exception
    @assert_stale_reference
    def screenshot(self, path):
        self.element.screenshot(path=path)
