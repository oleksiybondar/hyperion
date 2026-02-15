from typing import Optional, Callable, Any
from hyperiontf.ui.components.radiogroup.radigroup import Radiogroup
from hyperiontf.ui.components.tabs.tabs import Tabs
from hyperiontf.ui.decorators.element_accessor import element_property
from hyperiontf.ui.components.button.button import Button
from hyperiontf.ui.components.dropdown.dropdown import Dropdown
from hyperiontf.ui.components.table.table import Table


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


def table(
    locator_getter: Optional[Callable] = None,
) -> Any:
    """
    Decorator for declaring a reusable Table component on a Page Object.

    The decorated method must return a ``TableBySpec`` instance that
    declaratively defines:

    - the table root scope
    - how rows are located
    - how cells are located within each row
    - optional header cell locators
    - optional slot policy rules for heterogeneous cell materialization

    The decorator transforms the method into a read-only property that
    returns a lazily constructed :class:`Table` component instance.

    Usage
    -----

        @table
        def users(self) -> TableBySpec:
            return TableBySpec(
                root=By.id("users"),
                rows=By.css("tbody tr"),
                cells=By.css("td"),
                header_cells=By.css("thead th"),
            )

    The resulting property:

    - Is resolved lazily on first access
    - Is scoped to the owning Page Object instance
    - Preserves the declarative specification without eager element resolution
    - Enables row/cell navigation, slot-based materialization,
      and table-level assertions/verification

    Parameters
    ----------
    locator_getter:
        Optional function to decorate when the decorator is used without parentheses.

    Returns
    -------
    property
        A property that returns a :class:`Table` component instance.
    """
    return element_property(source_function=locator_getter, klass=Table)


def tabs(
    locator_getter: Optional[Callable] = None,
) -> Any:

    return element_property(source_function=locator_getter, klass=Tabs)
