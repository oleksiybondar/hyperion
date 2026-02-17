from typing import Optional

from hyperiontf.typing import LocatorTree
from hyperiontf.ui.components.button.spec import ButtonBySpec


class DropdownBySpec(ButtonBySpec):
    """
    Specification object for a Dropdown component.

    DropdownBySpec extends ButtonBySpec to model a dropdown as a
    **clickable trigger with externally resolved option components** and a
    **configurable selected-value resolution strategy**.

    By inheriting from ButtonBySpec, a dropdown explicitly separates:
    - the interaction target (root / trigger)
    - the identity or visible label (label, optional)

    In Hyperion terms, a dropdown consists of:
    - a trigger element that opens the dropdown and reflects the current selection
    - a collection of option components that may be rendered anywhere in the UI tree
    - a selected-value resolution strategy defining how the current value is read

    Parameters:
        root:
            Locator tree describing the dropdown trigger element.

            This element is responsible for:
            - receiving interaction events (click, keyboard)
            - opening and closing the dropdown menu
            - serving as a potential source of the selected value

        options:
            Locator tree describing the dropdown options.

            Options are modeled as a flat collection of Button-compatible
            components and are not required to be children of the trigger
            element. They may be rendered as siblings, overlays, portals, or
            at document scope.

            Resolution scope is fully controlled by the locator definition.

        label:
            Optional locator tree describing where the dropdown label or selected
            value should be resolved from.

            When provided, the label element may serve as:
            - the visible selected-value source
            - an alternative identity source when the trigger itself does not
              expose meaningful text

            When omitted, the trigger element is treated as the label source
            unless overridden by value resolution rules.

        option_label:
            Optional locator tree describing where each option's label/text
            should be resolved from.

            This is useful when an option container is clickable, but the
            human-readable text is rendered by a nested child element.

        value_attribute:
            Defines how the selected value should be resolved.

            Supported values:
            - "AUTO" (default):
                Use heuristic resolution based on the underlying control type
                and available locators.

                Typical heuristic behavior includes:
                - native <select>: resolve selected value via attribute (e.g. "value")
                - custom dropdowns: resolve text from label or trigger element
            - "text":
                Always resolve the selected value via visible text
                (label or trigger text).
            - any valid DOM attribute name (e.g. "value", "aria-label", "data-value"):
                Resolve the selected value by reading the specified attribute
                from the resolved value source.

            This field allows explicit override of automatic behavior when
            heuristic resolution is insufficient or ambiguous.

    Notes:
        - DropdownBySpec is a declarative description only; it performs no
          interaction, state resolution, or selection logic by itself.
        - Selected-value resolution is performed by the Dropdown component
          at runtime based on this specification.
        - Option scoping is entirely controlled by the locator definition;
          no implicit parent-child relationship between trigger and options
          is assumed.
        - Slot policies are not required for Dropdown components and are
          therefore not part of this specification.
    """

    def __init__(
        self,
        root: LocatorTree,
        options: LocatorTree,
        label: Optional[LocatorTree] = None,
        value_attribute: Optional[str] = "AUTO",
        option_label: Optional[LocatorTree] = None,
    ):
        super().__init__(root, label)
        self.options = options
        self.value_attribute = value_attribute
        self.option_label = option_label
