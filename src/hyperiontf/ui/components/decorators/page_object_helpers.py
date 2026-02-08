from typing import Optional, Callable, Any

from hyperiontf.ui.decorators.element_accessor import element_property
from hyperiontf.ui.components.button.button import Button
from hyperiontf.ui.components.dropdown.dropdown import Dropdown


def button(
    locator_getter: Optional[Callable] = None,
) -> Any:
    """
    Decorator for accessing a single UI element.

    This decorator is used to create a read-only property that returns an instance of the `Element` class. The decorated
    method should return the locator of the UI element.

    :param locator_getter: Optional function to decorate passed as a positional argument. (default: None)
    :return: Property that returns an instance of the `Element` class.
    """
    return element_property(source_function=locator_getter, klass=Button)


def dropdown(
    locator_getter: Optional[Callable] = None,
) -> Any:
    """
    Decorator for accessing a single UI element.

    This decorator is used to create a read-only property that returns an instance of the `Element` class. The decorated
    method should return the locator of the UI element.

    :param locator_getter: Optional function to decorate passed as a positional argument. (default: None)
    :return: Property that returns an instance of the `Element` class.
    """
    return element_property(source_function=locator_getter, klass=Dropdown)
