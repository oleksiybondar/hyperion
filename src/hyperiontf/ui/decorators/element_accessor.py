"""
Hyperion UI Element Creation Helper

This module contains utility functions and decorators for creating and managing UI elements in the Hyperion UI testing framework.

Decorators:
    - element_property: Converts a method returning an element locator into a read-only property returning an instance
                        of an element class (Element, Widget, IFrame, or WebView).

Helper Functions:
    - _create_element_instance: Creates and returns an instance of an element based on the given class and other
                                parameters.

Classes:
    None

Note:
    This module is intended to be used internally by the Hyperion UI testing framework. It provides utility functions
    and decorators to enhance the creation and management of UI elements in page object classes or page object modules.

"""

from hyperiontf.typing import AnyElement
from ..element import Element
from ..widget import Widget
from ..iframe import IFrame
from ..webview import WebView
from ..elements import Elements
from typing import Optional, Callable, Type, Union, Any, Tuple


def _create_element_instance(
    klass: AnyElement,
    parent: Any,
    locator: Any,
    name: str,
    is_list: bool,
) -> AnyElement:
    """
    Creates and returns an instance of an element based on the given class and other parameters.

    :param klass: The target class to be constructed.
    :param parent: The parent object that owns the element.
    :param locator: The locator used to identify the element.
    :param name: The name of the element.
    :param is_list: A flag indicating if it's a single element (False) or an array of elements (True).
    :return: An instance of the specified class (Element, Widget, IFrame, or WebView) or Elements if is_list is True.
    """
    if is_list:
        return Elements(parent, locator, name, klass)
    else:
        return klass(parent, locator, name)


def element_property(
    source_function: Optional[Callable] = None,
    klass: Optional[Type[Union[Element, Widget, IFrame, WebView]]] = Element,
    is_list: bool = False,
    is_memorized: bool = True,
) -> Union[Callable[[Callable[..., Tuple]], property], property]:
    """
    A parametrized decorator to convert a method into a read-only property returning an instance of an element.

    NOTE: This decorator is designed to be used in Page object classes or page object modules, and is not intended for
    direct usage.

    :param source_function: An optional function to decorate, passed as a positional argument. If provided, the decorator
    call is without additional parameters.
    :param klass: An optional target class to be constructed. The default is Hyperion::UI::Element.
    :param is_list: An optional flag indicating if it's a single element (False) or an array of elements (True).
    :param is_memorized: An optional flag to create an instance of the target class only when first accessed, otherwise
    create a new instance every time. The default is True.
    :return: A decorator or a read-only property of type Element or Elements.

    Usage:
    ------
    @element_property
    def get_element_locator(self):
        # Some code to obtain element locator
        return element_locator

    @element_property(klass=Widget, is_list=True)
    def get_widget_elements(self):
        # Some code to obtain a list of widget elements
        return widget_element_locators
    """

    def decorator(locator_getter: Callable) -> property:
        """
        The actual decorator that converts a method returning an element locator into a read-only property returning an
        instance of the Element class family.

        :param locator_getter: A function to be decorated.
        :return: A read-only property returning an instance of Element or Elements.
        """

        def locator_decorator(*args: Any, **kwargs: Any) -> Any:
            """
            Converts the method returning the element locator into a read-only property returning an instance of the
            Element class family.

            :return: An instance of Element or Elements, depending on the 'is_list' flag.
            """
            parent = args[0]
            locator = locator_getter(*args, **kwargs)
            name = locator_getter.__name__
            inner_name = f"_{name}_element"

            if is_memorized and hasattr(parent, inner_name):
                return getattr(parent, inner_name)

            element_instance = _create_element_instance(
                klass, parent, locator, name, is_list
            )

            if is_memorized:
                setattr(parent, inner_name, element_instance)

            return element_instance

        return property(locator_decorator)

    if source_function is None:
        return decorator

    return decorator(source_function)
