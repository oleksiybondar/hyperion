from typing import Optional, Callable, Any

from hyperiontf.ui.components.base_component import BaseComponent
from hyperiontf.ui.components.components import Components
from hyperiontf.ui.decorators.element_accessor import element_property


def components(
    locator_getter: Optional[Callable] = None,
    klass: Optional[Callable] = BaseComponent,
) -> Any:
    """
    Decorator for declaring a collection of reusable components.

    The decorated method must return a component specification object
    (for example, `TabsBySpec`, `TableBySpec`, or another `ComponentSpec`
    derivative) whose `root` points to a *collection locator*.

    This decorator creates a read-only property that returns a lazily resolved
    :class:`Components` collection, where each item is materialized as `klass`
    using an indexed clone of the returned spec.

    Usage:

        @components(klass=MyComponent)
        def cards(self):
            return CardBySpec(
                root=By.css(".card"),
                ...
            )

    Parameters:
        locator_getter:
            Optional function to decorate when used without parentheses.
        klass:
            Component class used for each collection item.
            Defaults to `BaseComponent`.

    Returns:
        property:
            Property resolving to a `Components` collection.
    """

    return element_property(
        source_function=locator_getter, list_klass=Components, klass=klass, is_list=True
    )
