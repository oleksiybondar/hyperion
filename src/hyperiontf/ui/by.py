"""
The 'By' module provides a convenient way to describe different mechanisms for locating elements on a web page. It
defines the 'By' class, which contains various class methods for creating locator instances based on different
location strategies, such as ID, name, class name, tag name, CSS selector, XPath selector, link text, partial link text,
test ID, and script.

Usage:
------
To create a locator using a specific strategy, you can directly call the respective class method of 'By'. For example:

    from selenium_framework.by import By

    # Create a locator to find an element by its ID attribute
    element_locator = By.id('element_id')

    # Create a locator to find an element using a CSS selector
    element_locator = By.css('#some_element')

    # Create a locator to find a link element with specific text
    link_locator = By.link_text('Click Me')

You can also modify the behavior of the locator by calling the 'from_document()' method to specify that the element
lookup should be performed in the entire document rather than within a parent element's context:

    element_locator = By.id('element_id').from_document()

The 'By' class is primarily used in web automation and testing frameworks for identifying and locating web elements.
It's designed to simplify the process of creating locators and improving the readability of test code.
"""

from hyperiontf.typing import LocatorStrategies, LocatorStrategiesType


class By:
    """
    Describes a mechanism for locating an element on the page.
    """

    def __init__(self, by: LocatorStrategiesType, value: str):
        """
        Initialize the By locator with the specified strategy and value.

        :param by: The name of the location strategy to use.
        :param value: The value to search for using the specified strategy.
        """
        self.by = by
        self.value = value
        self.search_scope = "parent"

    @classmethod
    def id(cls, value: str):
        """
        Creates a By locator that finds elements by their ID attribute.

        :param value: The ID to search for.
        :return: The new By locator.
        """
        return cls(LocatorStrategies.ID, value)

    @classmethod
    def name(cls, value: str):
        """
        Creates a By locator that finds elements by their 'name' attribute.

        :param value: The name attribute to search for.
        :return: The new By locator.
        """
        return cls(LocatorStrategies.NAME, value)

    @classmethod
    def class_name(cls, value: str):
        """
        Creates a By locator that finds elements by their class name.

        :param value: The class name to search for.
        :return: The new By locator.
        """
        return cls(LocatorStrategies.CLASS_NAME, value)

    @classmethod
    def tag(cls, value: str):
        """
        Creates a By locator that finds elements with a given tag name.

        :param value: The tag name to search for.
        :return: The new By locator.
        """
        return cls(LocatorStrategies.TAG_NAME, value)

    @classmethod
    def css(cls, value: str):
        """
        Creates a By locator that finds elements using a CSS selector.

        :param value: The CSS selector to use.
        :return: The new By locator.
        """
        return cls(LocatorStrategies.CSS_SELECTOR, value)

    @classmethod
    def xpath(cls, value: str):
        """
        Creates a By locator that finds elements matching an XPath selector. Care should be taken when using an XPath
        selector with an Element as Framework will respect the context specified in the selector. For example, given the
        selector `//div`, Framework will search from the document root regardless of whether the locator was used with a
        WebElement.

        :param value: The XPath selector to use.
        :return: The new By locator.
        """
        return cls(LocatorStrategies.XPATH, value)

    @classmethod
    def link_text(cls, value: str):
        """
        Creates a By locator that finds link elements whose `Element.text` equals the given substring.

        :param value: The link text to search for.
        :return: The new By locator.
        """
        return cls(LocatorStrategies.LINK_TEXT, value)

    @classmethod
    def partial_link_text(cls, value: str):
        """
        Creates a By locator that finds link elements whose `Element.text` contains the given substring.

        :param value: The link text to search for.
        :return: The new By locator.
        """
        return cls(LocatorStrategies.PARTIAL_LINK_TEXT, value)

    @classmethod
    def class_chain(cls, value: str):
        """
        Creates a By locator that finds elements using a iOS Class chain selector.

        :param value: The link text to search for.
        :return: The new By locator.
        """
        return cls(LocatorStrategies.IOS_CLASS_CHAINE, value)

    @classmethod
    def predicate(cls, value: str):
        """
        Creates a By locator that finds elements using a iOS Predicate.

        :param value: The link text to search for.
        :return: The new By locator.
        """
        return cls(LocatorStrategies.IOS_PREDICATE, value)

    @classmethod
    def test_id(cls, value: str):
        """
        Creates a By locator that finds elements using a test ID.

        :param value: The test ID to search for.
        :return: The new By locator.
        """
        return cls(LocatorStrategies.TEST_ID, value)

    @classmethod
    def script(cls, script: str):
        """
        Creates a By locator that finds elements by evaluating a script that defines the body of the `execute_script`
        method. The return value of this function must be an element or an array-like list of elements. When this locator
        returns a list of elements, but only one is expected, the first element in this list will be used as the single
        element value.

        :param script: The script to execute.
        :return: The new By locator.
        """
        return cls(LocatorStrategies.SCRIPT, script)

    @classmethod
    def accessibility_id(cls, accessibility_id: str):
        """
        Creates a By locator that finds elements by their Automation ID/Accessibility ID attribute.

        :param accessibility_id: windows accessibility id or automation id.
        :return: The new By locator.
        """
        return cls(LocatorStrategies.WINDOWS_ACCESSIBILITY_ID, accessibility_id)

    def from_document(self):
        """
        Specifies that the element lookup should be performed in the entire document rather than within a parent
        element's context.

        :return: The modified By locator.
        """
        self.search_scope = "document"
        return self

    def __str__(self):
        """
        Returns a string representation of the By locator.

        :return: The string representation of the By locator.
        """
        return f"By.{self.by}({self.value}), search scope: {self.search_scope}"
