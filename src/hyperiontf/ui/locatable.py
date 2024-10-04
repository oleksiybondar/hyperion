import re

from .by import By
from hyperiontf.typing import (
    IncorrectLocatorException,
    HyperionUIException,
    NoSuchElementException,
)
from hyperiontf.typing import LocatorStrategies

import time
from typing import Any, Sized, cast, Dict, Union

from hyperiontf.configuration import config
from hyperiontf.logging import getLogger

logger = getLogger("Element")


class LocatableElement:
    """
    Represents a locatable element within a web page or application. This class is responsible for locating and providing
    access to a specific element or a collection of elements based on the provided locator strategy.

    The `LocatableElement` class follows the single responsibility principle, separating the responsibility of locating
    elements from other aspects of the class.

    Attributes:
        parent (object): The parent element or container that contains this element.
        locator (By | dict): The locator strategy used to identify the element. It can be a `By` object or a dictionary
                             of locators categorized by platform, operating system, and viewport.
        name (str): A descriptive name for the element used for logging and identification purposes.

    Public Properties:
        platform (str): The platform of the element, determined by the document holder's platform.
        viewport (str): The viewport of the element, determined by the document holder's viewport.
        os (str): The operating system of the element, determined by the root element's operating system.
        root (object): The root element or container of the current element.
        document_holder (object): The document holder that contains this element.

    Methods:
        find_itself(retries: Optional[int] = config.element.search_attempts):
            Searches and locates the element based on the provided locator strategy.

    Private Methods:
        _fetch_elements_item(actual_locator: By | dict, retries: Optional[int] = config.element.search_attempts):
            Searches and locates multiple elements based on the provided locator strategy.
        _exec_search(actual_locator: By | dict, retries: Optional[int] = config.element.search_attempts):
            Executes the element search based on the provided locator strategy.
        _fetch_scope_object(actual_locator): Fetches the scope object for the element search based on the locator.
        _fetch_actual_locator(locator: Optional[By | dict] = None) -> By:
            Fetches the actual locator for the element search, considering platform, operating system, and viewport
            specific locators.
    """

    # Define a sentinel object to represent "not searched yet"
    _NOT_SEARCHED_YET = object()

    def __init__(self, parent, locator: By | dict, name: str):
        """
        Initialize a LocatableElement instance.

        Args:
            parent (object): The parent element or container that contains this element.
            locator (By | dict): The locator strategy used to identify the element. It can be a `By` object or a
                                 dictionary of locators categorized by platform, operating system, and viewport.
            name (str): A descriptive name for the element used for logging and identification purposes.
        """
        self.parent = parent
        self._locator = locator
        self._element_adapter: Any = self._NOT_SEARCHED_YET
        if bool(re.match("^\\d+$", name)):
            self.__full_name__ = f"{parent.__full_name__}[{name}]"
        else:
            self.__full_name__ = f"{parent.__full_name__}.{name}"

    @property
    def element_adapter(self) -> Any:
        """
        Get the element adapter representing the located element or elements.

        The `element_adapter` property performs an automatic search once someone tries to interact with the object.
        If the element is not searched yet, it will execute `find_itself()` method to locate the element.

        Returns:
            object or list: The element adapter representing the located element or elements.
        """
        if self._element_adapter is not self._NOT_SEARCHED_YET:
            return self._element_adapter

        # perform automatic search once someone tries to interact with object
        self.find_itself()
        return self._element_adapter

    @property
    def platform(self) -> str:
        """
        Get the platform of the element.

        The platform is determined by the document holder's platform. The platform specifies the environment in which the
        element is located, such as 'web', 'mobile', or 'desktop'.

        Returns:
            str: The platform of the element.
        """
        # do not use root as root platform may be one, but it has webview, so for that document platform will be
        # different
        return self.document_holder.platform

    @property
    def viewport(self) -> str:
        """
        Get the viewport of the element.

        The viewport is determined by the document holder's viewport. The viewport represents the size and layout of the
        viewable area in which the element is displayed, such as 'xs', 'sm', 'md', 'lg', or 'xl'.

        Returns:
            str: The viewport of the element.
        """
        # do not use root as root viewport may be bigger than its built-ins, like iFrames and WebViews, and their
        # dimensions are not necessarily equal to the app one
        return self.document_holder.viewport

    @property
    def os(self) -> str:
        """
        Get the operating system of the element.

        The operating system is determined by the root element's operating system. It represents the underlying operating
        system on which the application or web page is running.

        Returns:
            str: The operating system of the element.
        """
        return self.root.os

    @property
    def root(self) -> Any:
        """
        Get the root element or container of the current element.

        Returns:
            object: The root element or container.
        """
        if hasattr(self.parent, "root"):
            return self.parent.root

        return self.parent

    @property
    def document_holder(self):
        """
        Get the document holder that contains this element.

        The document holder is the top-level element or container that encapsulates the entire page or application.

        Returns:
            object: The document holder that contains this element.
        """
        node = self.parent
        while hasattr(node, "parent"):
            if hasattr(node, "context_manager") or hasattr(node, "content_manager"):
                return node
            node = node.parent
        return node

    @property
    def contains_multiple_elements(self):
        """
        Check if the Elements instance contains multiple elements.

        Returns:
            bool: True if the Elements instance contains multiple elements, False otherwise.
        """
        return hasattr(self, "_elements_cache")

    @property
    def is_multi_child(self):
        """
        Get a boolean value indicating whether this SingleElement is a child of a MultipleElement.

        A SingleElement can be part of a MultipleElement, which represents a collection of elements.
        If this property returns True, it means the SingleElement is part of a MultipleElement;
        otherwise, it is not associated with a MultipleElement.

        Returns:
            bool: True if this SingleElement is a child of a MultipleElement, False otherwise.
        """
        if hasattr(self.parent, "contains_multiple_elements"):
            return self.parent.contains_multiple_elements

        return False

    def find_itself(self, retries: int = config.element.search_attempts):
        """
        Searches and locates the element based on the provided locator strategy.

        Args:
            retries (int, optional): The number of retries for element search in case of failure. Defaults to
                                     `config.element.search_attempts`.

        Raises:
            NoSuchElementException: If the element is not found after the specified number of retries.
        """
        if hasattr(self.parent, "__resolve__"):
            self.parent.__resolve__()

        actual_locator = self._resolve_locator()

        # applicable only for Multiple Element children
        if actual_locator.by == LocatorStrategies.ELEMENTS_ITEM:
            self._fetch_elements_item(actual_locator)
        else:
            self._exec_search(actual_locator, retries)

    def _resolve_locator(self):
        if self._locator is not None:
            return self._fetch_actual_locator(self._locator)
        if self._locator is None and hasattr(self, "default_locator"):
            return self._fetch_actual_locator(self.default_locator)
        else:
            raise Exception("No Locator")

    def _fetch_elements_item(
        self,
        actual_locator: Any,
        retries: int = config.element.search_attempts,
    ):
        """
        Searches and locates multiple elements based on the provided locator strategy.

        Args:
            actual_locator (By | dict): The actual locator strategy used to identify the elements.
            retries (int, optional): The number of retries for element search in case of failure. Defaults to
                                     `config.element.search_attempts`.

        Raises:
            NoSuchElementException: If the element is not found after the specified number of retries.
        """
        try:
            self._element_adapter = self.parent.element_adapter[
                int(actual_locator.value)
            ]
        except IndexError:
            self.parent.find_itself()
            if retries > 0:
                return self.find_itself(retries - 1)
            else:
                raise NoSuchElementException(
                    f"[{self.parent.__full_name__}] have only {len(self.parent)} items, but"
                    f" requested item index is {actual_locator.value}"
                )

    def _exec_search(
        self,
        actual_locator: By | dict,
        retries: int = config.element.search_attempts,
    ):
        """
        Executes the element search based on the provided locator strategy.

        Args:
            actual_locator (By | dict): The actual locator strategy used to identify the element.
            retries (int, optional): The number of retries for element search in case of failure. Defaults to
                                     `config.element.search_attempts`.

        Raises:
            NoSuchElementException: If the element is not found after the specified number of retries.
        """
        # If elements require resolving the window handle/context/content before the search itself,
        # then its parent must implement the __resolve__ method. Otherwise, no extra actions are needed,
        # and we can directly fire the find call.

        search_scope = self._fetch_scope_object(actual_locator)
        # do not try to search child element for error elements
        if isinstance(search_scope, HyperionUIException):
            raise search_scope

        logger.debug(f"[{self.__full_name__}] Searching element by {actual_locator}")
        try:
            # Elements cache is a specific attribute for the Elements class family, checking by class will cause a
            # cyclomatic import error since Elements class is also a child of the LocatableElement class.
            if self.contains_multiple_elements:
                self._exec_multiple_search(search_scope, actual_locator, retries)
            else:
                self._element_adapter = search_scope.find_element(actual_locator)
        except HyperionUIException as uie:
            self._resolve_search_exception(actual_locator, uie, retries)

    def _exec_multiple_search(self, search_scope, actual_locator, retries):
        self._element_adapter = cast(Sized, search_scope.find_elements(actual_locator))
        # For an array of elements, we need to know the count, so log it.
        logger.debug(
            f"[{self.__full_name__}] {len(self._element_adapter)} elements found"
        )
        # Normally, find elements does not raise any exception.
        if len(self._element_adapter) == 0 and retries > 0:
            time.sleep(config.element.search_retry_timeout)
            return self.find_itself(retries - 1)

    def _resolve_search_exception(self, actual_locator, exception, retries):
        # During retries, different exceptions may occur, so for debug purposes, we need to log them all.
        logger.debug(
            f"[{self.__full_name__}] Exception intercepted! {exception.__class__.__name__}: {exception}"
        )
        if retries > 0:
            if (
                exception.__class__.__name__ == "StaleElementReferenceException"
                and hasattr(self.parent, "find_itself")
            ):
                if self.parent.is_multi_child:
                    self.parent.parent.find_itself()
                self.parent.find_itself()
            else:
                time.sleep(config.element.search_retry_timeout)
            return self.find_itself(retries - 1)
        else:
            self._element_adapter = NoSuchElementException(
                f"[{self.__full_name__}] Element was not found!\n"
                f"Locator: {actual_locator}"
            )

    def _fetch_scope_object(self, actual_locator):
        """
        Fetches the scope object for the element search based on the locator.

        The scope object is determined based on the locator's search scope. If the search scope is 'document', the root
        element's automation adapter is returned. Otherwise, if the parent element has an automation adapter, it is
        returned. Otherwise, the parent element's element adapter is returned.

        Explanation:
        This method needs to check if self.parent is an instance of the IFrame class. However, IFrame is a child class of
        LocatableElement. Placing the import of IFrame at the top of the file would lead to a cyclic import issue.

        Cyclic imports occur when two or more modules depend on each other, directly or indirectly. In this case, if
        IFrame is imported at the top of the file that contains LocatableElement, and IFrame imports LocatableElement,
        it creates a circular dependency that Python cannot resolve.

        To avoid this, the import of IFrame is placed within the method _fetch_scope_object. This ensures that the
        IFrame class is only imported when this method is executed and not during the initial module import. By
        doing so, we prevent the cyclic import issue, and the code remains functional without any import errors.

        Args:
            actual_locator (By | dict): The actual locator strategy used to identify the element.

        Returns:
            object: The scope object used for element search.
        """
        from .iframe import IFrame

        if actual_locator.search_scope == "document":
            return self.root.automation_adapter

        if isinstance(self.parent, IFrame):
            return self.root.automation_adapter

        if hasattr(self.parent, "automation_adapter"):
            return self.parent.automation_adapter

        return self.parent.element_adapter

    def _fetch_actual_locator(self, locator: Union[By, Dict[str, Any]]) -> By:
        """
        Initiates the process of fetching the actual locator for the element search,
        considering platform, operating system, and viewport specific locators.

        Args:
            locator (By | dict): The locator strategy to be resolved.

        Returns:
            By: The resolved actual locator strategy.
        """
        if isinstance(locator, dict):
            return self._fetch_platform_specific_locator(locator)
        return locator

    def _fetch_platform_specific_locator(self, locator: Dict[str, Any]) -> By:
        """
        Checks for a platform-specific locator and delegates to the next
        level if not found.

        Args:
            locator (dict): Locator dictionary.

        Returns:
            By: The resolved actual locator strategy.
        """
        if self.platform in locator:
            return self._fetch_actual_locator(locator[self.platform])
        return self._fetch_os_specific_locator(locator)

    def _fetch_os_specific_locator(self, locator: Dict[str, Any]) -> By:
        """
        Checks for an operating system-specific locator and delegates to the next
        level if not found.

        Args:
            locator (dict): Locator dictionary.

        Returns:
            By: The resolved actual locator strategy.
        """
        if self.os in locator:
            return self._fetch_actual_locator(locator[self.os])
        return self._fetch_viewport_specific_locator(locator)

    def _fetch_viewport_specific_locator(self, locator: Dict[str, Any]) -> By:
        """
        Checks for a viewport-specific locator and delegates to the default
        locator if not found.

        Args:
            locator (dict): Locator dictionary.

        Returns:
            By: The resolved actual locator strategy.
        """
        if self.viewport in locator:
            return self._fetch_actual_locator(locator[self.viewport])
        return self._fetch_default_locator(locator)

    def _fetch_default_locator(self, locator: Dict[str, Any]) -> By:
        """
        Checks for a default locator. If not found, raises an exception.

        Args:
            locator (dict): Locator dictionary.

        Returns:
            By: The resolved actual locator strategy.

        Raises:
            IncorrectLocatorException: If no suitable locator is found.
        """
        if "default" in locator:
            return self._fetch_actual_locator(locator["default"])

        raise IncorrectLocatorException(
            f"[{self.__full_name__}] Does not contain a locator for '{self.platform}' "
            f"platform, '{self.os}' operating system, and '{self.viewport}' viewport"
        )
