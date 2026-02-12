from typing import Optional, Callable, Any
from hyperiontf.ui.decorators.element_accessor import element_property
from hyperiontf.ui.components.slots import Slots


def slots(
    locator_getter: Optional[Callable] = None,
    klass: Optional[Callable] = Slots,
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
    return element_property(
        source_function=locator_getter, list_klass=klass, is_list=True
    )
