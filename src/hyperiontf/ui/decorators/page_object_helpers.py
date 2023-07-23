"""
Hyperion Simplified Decorators for UI Element Access

This module provides a set of simplified decorators that enable easy access and management of UI elements in the Hyperion UI
testing framework. The decorators make use of the more general `element_property` decorator from the `element_accessor`
module and provide specific configurations for different types of UI elements, including single elements and lists of elements.

Decorators:
    - element: Decorator for accessing a single UI element.
    - elements: Decorator for accessing a list of UI elements.
    - widget: Decorator for accessing a single widget UI element.
    - widgets: Decorator for accessing a list of widget UI elements.
    - iframe: Decorator for accessing a single iframe UI element.
    - iframes: Decorator for accessing a list of iframe UI elements.
    - webview: Decorator for accessing a single webview UI element.
    - webviews: Decorator for accessing a list of webview UI elements.
    - dynamic: Decorator for accessing a single UI element without memorization (creates new instance every time).
    - dynamics: Decorator for accessing a list of UI elements without memorization (creates new instances every time).

Note:
    These decorators are designed to be used in page object classes or page object modules in the Hyperion UI testing framework.
    They provide a convenient way to access UI elements in different configurations (single, lists, dynamic, etc.).
"""

from .element_accessor import element_property
from ..element import Element
from ..iframe import IFrame
from ..widget import Widget
from ..webview import WebView
from typing import Optional, Type, Union, Callable, Any


def element(
    locator_getter: Optional[Callable] = None,
) -> Any:
    """
    Decorator for accessing a single UI element.

    This decorator is used to create a read-only property that returns an instance of the `Element` class. The decorated
    method should return the locator of the UI element.

    :param locator_getter: Optional function to decorate passed as a positional argument. (default: None)
    :return: Property that returns an instance of the `Element` class.
    """
    return element_property(source_function=locator_getter, klass=Element)


def elements(
    locator_getter: Optional[Callable] = None,
) -> Any:
    """
    Decorator for accessing a list of UI elements.

    This decorator is used to create a read-only property that returns a list of instances of the `Elements` class.
    The decorated method should return the locator of the UI elements.

    :param locator_getter: Optional function to decorate passed as a positional argument. (default: None)
    :return: Property that returns a list of instances of the `Elements` class.
    """
    return element_property(source_function=locator_getter, klass=Element, is_list=True)


def widget(
    locator_getter: Optional[Callable] = None, klass: Optional[Type[Widget]] = Widget
) -> Any:
    """
    Decorator for accessing a single widget UI element.

    This decorator is used to create a read-only property that returns an instance of the specified widget class.
    The decorated method should return the locator of the widget UI element.

    :param locator_getter: Optional function to decorate passed as a positional argument. (default: None)
    :param klass: Optional target class to be constructed. (default: `Widget`)
    :return: Property that returns an instance of the specified widget class.
    """
    return element_property(source_function=locator_getter, klass=klass)


def widgets(
    locator_getter: Optional[Callable] = None, klass: Optional[Type[Widget]] = Widget
) -> Any:
    """
    Decorator for accessing a list of widget UI elements.

    This decorator is used to create a read-only property that returns a list of instances of the specified widget class.
    The decorated method should return the locator of the widget UI elements.

    :param locator_getter: Optional function to decorate passed as a positional argument. (default: None)
    :param klass: Optional target class to be constructed. (default: `Widget`)
    :return: Property that returns a list of instances of the specified widget class.
    """
    return element_property(source_function=locator_getter, klass=klass, is_list=True)


def iframe(
    locator_getter: Optional[Callable] = None, klass: Optional[Type[IFrame]] = IFrame
) -> Any:
    """
    Decorator for accessing a single iframe UI element.

    This decorator is used to create a read-only property that returns an instance of the specified iframe class.
    The decorated method should return the locator of the iframe UI element.

    :param locator_getter: Optional function to decorate passed as a positional argument. (default: None)
    :param klass: Optional target class to be constructed. (default: `IFrame`)
    :return: Property that returns an instance of the specified iframe class.
    """
    return element_property(source_function=locator_getter, klass=klass)


def iframes(
    locator_getter: Optional[Callable] = None, klass: Optional[Type[IFrame]] = IFrame
) -> Any:
    """
    Decorator for accessing a list of iframe UI elements.

    This decorator is used to create a read-only property that returns a list of instances of the specified iframe class.
    The decorated method should return the locator of the iframe UI elements.

    :param locator_getter: Optional function to decorate passed as a positional argument. (default: None)
    :param klass: Optional target class to be constructed. (default: `IFrame`)
    :return: Property that returns a list of instances of the specified iframe class.
    """
    return element_property(source_function=locator_getter, klass=klass, is_list=True)


def webview(
    locator_getter: Optional[Callable] = None, klass: Optional[Type[WebView]] = WebView
) -> Any:
    """
    Decorator for accessing a single webview UI element.

    This decorator is used to create a read-only property that returns an instance of the specified webview class.
    The decorated method should return the locator of the webview UI element.

    :param locator_getter: Optional function to decorate passed as a positional argument. (default: None)
    :param klass: Optional target class to be constructed. (default: `WebView`)
    :return: Property that returns an instance of the specified webview class.
    """
    return element_property(source_function=locator_getter, klass=klass)


def webviews(
    locator_getter: Optional[Callable] = None, klass: Optional[Type[WebView]] = WebView
) -> Any:
    """
    Decorator for accessing a list of webview UI elements.

    This decorator is used to create a read-only property that returns a list of instances of the specified webview class.
    The decorated method should return the locator of the webview UI elements.

    :param locator_getter: Optional function to decorate passed as a positional argument. (default: None)
    :param klass: Optional target class to be constructed. (default: `WebView`)
    :return: Property that returns a list of instances of the specified webview class.
    """
    return element_property(source_function=locator_getter, klass=klass, is_list=True)


def dynamic(
    locator_getter: Optional[Callable] = None,
    klass: Optional[Type[Union[Element, Widget, IFrame, WebView]]] = Element,
) -> Any:
    """
    Decorator for accessing a single UI element without memorization (creates new instance every time).

    This decorator is used to create a read-only property that returns a new instance of the specified target class
    every time it is accessed. The decorated method should return the locator of the UI element.

    :param locator_getter: Optional function to decorate passed as a positional argument. (default: None)
    :param klass: Optional target class to be constructed. (default: `Element`)
    :return: Property that returns a new instance of the specified target class every time it is accessed.
    """
    return element_property(
        source_function=locator_getter, klass=klass, is_memorized=False
    )


def dynamics(
    locator_getter: Optional[Callable] = None,
    klass: Optional[Type[Union[Element, Widget, IFrame, WebView]]] = Element,
) -> Any:
    """
    Decorator for accessing a list of UI elements without memorization (creates new instances every time).

    This decorator is used to create a read-only property that returns a new list of instances of the specified target class
    every time it is accessed. The decorated method should return the locator of the UI elements.

    :param locator_getter: Optional function to decorate passed as a positional argument. (default: None)
    :param klass: Optional target class to be constructed. (default: `Element`)
    :return: Property that returns a new list of instances of the specified target class every time it is accessed.
    """
    return element_property(
        source_function=locator_getter,
        klass=klass,
        is_list=True,
        is_memorized=False,
    )
