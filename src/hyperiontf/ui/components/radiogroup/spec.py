from typing import Optional

from hyperiontf.typing import LocatorTree
from hyperiontf.ui.components.spec import ComponentSpec


class RadioGroupBySpec(ComponentSpec):
    """
    Specification object for a RadioGroup component.

    RadioGroupBySpec describes the structural locators required to model a group
    of radio options as a reusable UI component.

    A RadioGroup consists of:
    - a logical root that scopes the group
    - a collection of radio items
    - an input element used as the state source
    - an optional label element used as the interaction target and text source

    Parameters:
        root:
            Locator tree describing the logical scope of the radio group.
            This may be a form, fieldset, or any meaningful container.

        items:
            Locator tree describing the collection of radio items.
            Items may represent inputs, labels, or wrapper elements depending
            on the DOM structure.

        input:
            Locator tree describing the radio input element relative to each item.
            The input is treated as the authoritative state source.

        label:
            Optional locator tree describing the label element relative to each item.
            When provided, the label is typically used as the interaction target
            and identity source. When omitted, the item root itself may serve
            as the identity source.

    Notes:
        - RadioGroupBySpec is a declarative description only; it performs no
          interaction or state resolution by itself.
        - The specification supports common real-world patterns, including:
            - label wrapping input
            - input/label sibling relationships
            - absence of a dedicated item wrapper
        - Interpretation of item structure is controlled entirely by locator design.
    """

    def __init__(
        self,
        root: LocatorTree,
        items: LocatorTree,
        input: LocatorTree,
        label: Optional[LocatorTree],
    ):
        super().__init__(root)
        self.items = items
        self.input = input
        self.label = label
