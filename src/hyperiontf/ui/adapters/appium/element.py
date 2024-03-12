from .map_locator import map_locator
from .map_exception import map_exception
from hyperiontf.ui import By
from hyperiontf.typing import LocatorStrategies, UnsupportedLocatorException


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
    def text(self):
        """
        Get the visible text of the element.

        Returns:
            str: The visible text of the element.

        Raises:
            HyperionException: If an error occurs while retrieving the text.

        """
        return self.element.text

    @property
    @map_exception
    def is_displayed(self):
        """
        Check if the element is displayed on the page.

        Returns:
            bool: True if the element is displayed, False otherwise.

        Raises:
            HyperionException: If an error occurs while checking the display status.

        """
        return self.element.is_displayed()

    @property
    @map_exception
    def is_enabled(self):
        """
        Check if the element is enabled and can be interacted with.

        Returns:
            bool: True if the element is enabled and can be interacted with, False otherwise.

        Raises:
            HyperionException: If an error occurs while checking the enabled status.

        """
        return self.element.is_enabled()

    @property
    @map_exception
    def is_selected(self):
        """
        Check if the element is selected (e.g., a checkbox or radio button is checked).

        Returns:
            bool: True if the element is selected, False otherwise.

        Raises:
            HyperionException: If an error occurs while checking the selected status.

        """
        return self.element.is_selected()

    @property
    @map_exception
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
        return self.element.size

    @property
    @map_exception
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
        return self.element.location

    @property
    @map_exception
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
        return self.element.location

    @property
    @map_exception
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
        return self.element.rect

    @map_exception
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
        selenium_locator = map_locator(locator.by)
        if selenium_locator == LocatorStrategies.UNSUPPORTED:
            raise UnsupportedLocatorException(
                f"Unsupported {locator.by} locator for Appium"
            )
        return Element(
            self.element.find_element(selenium_locator, locator.value), self.page
        )

    @map_exception
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
        selenium_locator = map_locator(locator.by)
        if selenium_locator == LocatorStrategies.UNSUPPORTED:
            raise UnsupportedLocatorException(
                f"Unsupported {locator.by} locator for Appium"
            )
        else:
            elements = self.element.find_elements(selenium_locator, locator.value)
        return list(map(lambda x: Element(x, self.page), elements))

    @map_exception
    def send_keys(self, data):
        """
        Simulate typing the specified data into the element.

        Args:
            data (str): The text to be typed into the element.

        Raises:
            HyperionException: If any exception occurs during sending the keys.
        """
        self.element.send_keys(data)

    @map_exception
    def click(self):
        """
        Perform a click action on the element.

        Raises:
            HyperionException: If any exception occurs during the click action.
        """
        self.element.click()

    @map_exception
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
        return self.element.get_attribute(name)

    @map_exception
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
        return self.element.value_of_css_property(name)

    @map_exception
    def clear(self):
        """
        Clear the input value of the element (if applicable).

        Raises:
            HyperionException: If any exception occurs during clearing the input value.
        """
        self.element.clear()

    @map_exception
    def submit(self):
        """
        Submit the form associated with the element (if applicable).

        Raises:
            HyperionException: If any exception occurs during the form submission.
        """
        self.element.submit()

    @property
    @map_exception
    def screenshot_as_base64(self):
        return self.element.screenshot_as_base64

    @map_exception
    def screenshot(self, path):
        return self.element.screenshot(path)
