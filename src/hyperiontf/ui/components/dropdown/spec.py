from hyperiontf.typing import LocatorTree
from hyperiontf.ui.components.component_specification import ComponentSpec


class DropdownBySpec(ComponentSpec):
    """
    Specification object for a Dropdown component.

    DropdownBySpec describes the structural locators required to model a dropdown
    as a reusable UI component.

    In Hyperion terms, a dropdown consists of:
    - a root element that acts as both the trigger and the selected-value source
    - a collection of option elements that may be located anywhere in the DOM

    Parameters:
        root:
            Locator tree describing the dropdown trigger.
            This element is responsible for opening the dropdown and reflecting
            the currently selected value.

        options:
            Locator tree describing the dropdown options.
            Options are modeled as a flat collection and are not required to be
            children of the root element. They may be rendered as siblings,
            overlays, or in a document-level portal.

    Notes:
        - DropdownBySpec is a declarative description only; it performs no
          interaction or state management.
        - Option scoping is entirely controlled by the locator definition;
          no implicit parent-child relationship is assumed.
        - Slot policies are not required for Dropdown and are therefore not
          part of this specification.
    """

    def __init__(self, root: LocatorTree, options: LocatorTree):
        super().__init__(root)
        self.options = options
