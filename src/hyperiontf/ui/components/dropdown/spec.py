from typing import Optional

from hyperiontf.typing import LocatorTree
from hyperiontf.ui.components.button.spec import ButtonBySpec


class DropdownBySpec(ButtonBySpec):
    """
    Specification object for a Dropdown component.

    DropdownBySpec extends ButtonBySpec to model a dropdown as a
    **clickable trigger with externally resolved options**.

    By inheriting from ButtonBySpec, a dropdown explicitly separates:
    - the interaction target (root / trigger)
    - the identity or visible label (label, optional)

    In Hyperion terms, a dropdown consists of:
    - a trigger element that opens the dropdown and reflects the current selection
    - a collection of option elements that may be rendered anywhere in the UI tree

    Parameters:
        root:
            Locator tree describing the dropdown trigger element.
            This element is responsible for opening the dropdown and receiving
            interaction events.

        options:
            Locator tree describing the dropdown options.
            Options are modeled as a flat collection and are not required to be
            children of the trigger element. They may be rendered as siblings,
            overlays, portals, or at document scope.

        label:
            Optional locator tree describing where the dropdown label or selected
            value should be resolved from.

            When omitted, the trigger element itself is treated as the label
            source by default.

    Notes:
        - DropdownBySpec is a declarative description only; it performs no
          interaction, state resolution, or selection logic by itself.
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
    ):
        super().__init__(root, label)
        self.options = options
