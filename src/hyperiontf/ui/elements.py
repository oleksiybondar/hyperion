from typing import Optional

from hyperiontf.logging import getLogger
from hyperiontf.typing import NoSuchElementException
from .element import Element
from .locatable import LocatableElement
from .by import By
from .eql.executor import evaluate
from .eql.parser import parse
from hyperiontf.typing import LocatorStrategies
from ..helpers.decorators.wait import wait

logger = getLogger("Element")


class Elements(LocatableElement):
    def __init__(self, parent, locator, name, item_class=Element):
        super().__init__(parent, locator, name)
        self._item_class = item_class
        self._elements_cache = []
        self._wait_previous_elements_count: Optional[int] = None

    def __resolve_eql_chain__(self, chain):
        if chain[0]["type"] == "attribute" and chain[0]["name"] == "length":
            return len(self._elements)

        if len(self._elements) == 0:
            return None

        if len(self._elements) < chain[0]["index"]:
            return None

        return self._elements[chain[0]["index"]].__resolve_eql_chain__(chain[1:])

    def __is_interactive__(self):
        if self.element_adapter is NoSuchElementException:
            raise self.element_adapter

    def __is_present__(self):
        if isinstance(self.element_adapter, NoSuchElementException):
            return False

        return self.__len__() > 0

    @property
    def is_present(self):
        return self.__is_present__()

    @property
    def _elements(self):
        if len(self.element_adapter) != len(self._elements_cache):
            self._cache_elements()

        return self._elements_cache

    def force_refresh(self):
        self._elements_cache = []
        self.find_itself()

    def _cache_elements(self):
        i = 0
        self._elements_cache = []
        while i < len(self.element_adapter):
            item = self._item_class(
                self, By(LocatorStrategies.ELEMENTS_ITEM, str(i)), str(i)
            )
            self._elements_cache.append(item)
            i += 1

    def __len__(self):
        return len(self.element_adapter)

    def __getitem__(self, index: int | str):
        if isinstance(index, str):
            return self.__getitem_by_eql__(index)

        return self._elements[index]

    def __getitem_by_eql__(self, query: str):
        parsed_query = parse(query)
        for element in self._elements:
            if evaluate(parsed_query, element):
                return element

        return None

    def __iter__(self):
        return iter(self._elements)

    def __contains__(self, item):
        return item in self._elements

    def index(self, item):
        return self._elements.index(item)

    def count(self, item):
        return self._elements.count(item)

    def sort(self, key=None, reverse=False):
        self._elements.sort(key=key, reverse=reverse)

    @wait()
    def wait_until_found(self):
        """
        Waits until at least one element is found on the page. This method will continuously attempt to find the elements until at least one is present or the specified timeout is reached.

        Parameters:
        - timeout (float, optional): The maximum time in seconds to wait for at least one element to be found. If not specified, a default timeout will be used.
        - raise_exception (bool, optional): If set to True, an exception will be raised if no elements are found within the timeout period. If False or not specified, no exception will be raised, and the method will return False if the elements are not found.

        Returns:
            bool: True if at least one element is found within the timeout, False otherwise.

        Note:
            This method utilizes a retry mechanism with a sleep interval between attempts to find the elements. The exact behavior regarding timeouts and exception handling can be adjusted by the `timeout` and `raise_exception` parameters.
        """
        if not self.__is_present__():
            self.find_itself()
            return False

        return True

    @wait()
    def wait_until_missing(self):
        """
        Waits until all elements are no longer found in the DOM or on the page. This method continuously checks for the absence of elements until none are present or the specified timeout is reached.

        Parameters:
        - timeout (float, optional): The maximum time in seconds to wait for all elements to be missing. If not specified, a default timeout value is used.
        - raise_exception (bool, optional): If set to True, an exception will be raised if any elements are still found after the timeout period. If False or not specified, no exception will be raised, and the method will return False if any elements are still found.

        Returns:
            bool: True if no elements are found within the timeout, False otherwise.
        """
        if self.__is_present__():
            self.find_itself()

        return self.__len__() == 0

    @wait()
    def wait_until_items_count(self, expected_count: int):
        """
        Waits until the count of elements matches the specified expected count. This method is useful for situations where a specific number of elements are expected to be present on the page.

        Parameters:
        - expected_count (int): The exact number of elements expected to be found.
        - timeout (float, optional): The maximum time in seconds to wait for the elements' count to match the expected count. If not specified, a default timeout value is used.
        - raise_exception (bool, optional): If set to True, an exception will be raised if the elements' count does not match the expected count within the timeout period. If False or not specified, no exception will be raised, and the method will return False if the count does not match.

        Returns:
            bool: True if the count of elements matches the expected count within the timeout, False otherwise.
        """
        if self.__len__() != expected_count:
            self.find_itself()

        return self.__len__() == expected_count

    @wait()
    def wait_until_items_decrease(self):
        """
        Waits until the count of elements decreases from its initial count. This method assumes elements have been previously found; it is not intended for initial element finding, for which `wait_until_found` should be used instead. The method continuously checks if the number of elements has decreased by at least one from the initial count.

        Parameters:
        - timeout (float, optional): The maximum time in seconds to wait for the elements' count to decrease. If not specified, a default timeout value is used.
        - raise_exception (bool, optional): If set to True, an exception will be raised if the elements' count does not decrease within the timeout period. If False or not specified, no exception will be raised, and the method will return False if the count remains the same or increases.

        Returns:
            bool: True if the count of elements decreases by at least one from the initial count within the timeout, False otherwise.
        """
        current_count = self.__len__()
        if (
            self._wait_previous_elements_count is None
            or current_count >= self._wait_previous_elements_count
        ):
            self._wait_previous_elements_count = current_count
            self.find_itself()
            return False

        self._wait_previous_elements_count = None
        return True

    @wait()
    def wait_until_items_increase(self):
        """
        Waits until the count of elements increases from its initial count. This method assumes elements have been previously found; it is not intended for initial element finding, for which `wait_until_found` should be used instead. The method continuously checks if the number of elements has increased by at least one from the initial count.

        Parameters:
        - timeout (float, optional): The maximum time in seconds to wait for the elements' count to increase. If not specified, a default timeout value is used.
        - raise_exception (bool, optional): If set to True, an exception will be raised if the elements' count does not increase within the timeout period. If False or not specified, no exception will be raised, and the method will return False if the count remains the same or decreases.

        Returns:
            bool: True if the count of elements increases by at least one from the initial count within the timeout, False otherwise.
        """
        current_count = self.__len__()
        if (
            self._wait_previous_elements_count is None
            or current_count <= self._wait_previous_elements_count
        ):
            self._wait_previous_elements_count = current_count
            self.find_itself()
            return False

        self._wait_previous_elements_count = None
        return True

    @wait()
    def wait_until_items_change(self):
        """
        Waits until the count of elements changes from its initial value. This method is useful for detecting when the number of elements on the page has been dynamically updated.

        Parameters:
        - timeout (float, optional): The maximum time in seconds to wait for the number of elements to change. If not specified, a default timeout value is used.
        - raise_exception (bool, optional): If set to True, an exception will be raised if the count of elements does not change within the timeout period. If False or not specified, no exception will be raised, and the method will return False if the count remains unchanged.

        Returns:
            bool: True if the count of elements changes within the timeout, False otherwise.
        """
        current_count = self.__len__()
        if (
            self._wait_previous_elements_count is None
            or current_count == self._wait_previous_elements_count
        ):
            self._wait_previous_elements_count = current_count
            self.find_itself()
            return False

        self._wait_previous_elements_count = None
        return True
