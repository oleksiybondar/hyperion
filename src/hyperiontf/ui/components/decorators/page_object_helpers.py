from typing import Optional, Callable, Any

from hyperiontf.ui import Element
from hyperiontf.ui.components.radiogroup.radigroup import Radiogroup
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


def radiogroup(
    locator_getter: Optional[Callable] = None,
) -> Any:
    """
    Decorator for declaring a reusable RadioGroup component on a Page Object.

    This decorator creates a read-only property that returns an instance of
    the `Radiogroup` component. The decorated method must return a
    `RadioGroupBySpec` instance describing the structure of the group.

    Usage:

        @radiogroup
        def notifications(self) -> RadioGroupBySpec:
            return RadioGroupBySpec(
                root=By.id("notifications"),
                items=By.css(".radio-item"),
                input=By.css("input[type='radio']"),
                label=By.css("label"),
            )

    The resulting property:

        - Is resolved lazily
        - Is scoped to the owning Page Object
        - Uses the provided specification to model item structure and state logic

    :param locator_getter:
        Optional function to decorate when used without parentheses.
        (default: None)

    :return:
        A property that returns an instance of the `Radiogroup` component.
    """
    return element_property(source_function=locator_getter, klass=Radiogroup)


def slots(
    locator_getter: Optional[Callable] = None,
) -> Any:
    """
    Decorator creating a read-only structured collection of component slots.

    The decorated method must return a locator identifying a group of UI nodes.
    Accessing the property returns a `Slots` collection whose items are resolved
    dynamically according to the parent component specification.

    Unlike `elements`/`widgets` collections, the resulting collection is
    heterogeneous: each position is interpreted as a structural role rather
    than a uniform item. The concrete object type for every index is determined
    by the parent component's `slot_resolver` using `SlotPolicyRule`s.

    Notes
    -----
    * The `Element` class passed to the underlying factory is only a placeholder
      required for initialization and caching.
    * The final instance type of each item is selected at runtime by the slot
      resolution policy.
    * The owning object must implement a `component_spec` property returning
      a `ComponentSpec`.

    :param locator_getter:
        Optional decorated function returning a locator for the slot container.
    :return:
        A read-only property resolving to a structured `Slots` collection.
    """
    return element_property(source_function=locator_getter, klass=Element, is_list=True)
