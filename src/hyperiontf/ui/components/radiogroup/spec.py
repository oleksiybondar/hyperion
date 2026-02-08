from typing import Optional

from hyperiontf.typing import LocatorTree
from hyperiontf.ui.components.button.spec import ButtonBySpec


class RadioGroupBySpec(ButtonBySpec):
    """
    Specification object for a RadioGroup component.

    RadioGroupBySpec defines the **declarative structure** required to model
    a group of radio options in a backend-agnostic and DOM-agnostic way.

    The specification intentionally supports real-world UI variability where:
    - a dedicated item wrapper may or may not exist
    - the radio input may or may not be directly addressable
    - the clickable label and the state source may be different elements

    A RadioGroup specification consists of:
    - a logical root that scopes the group
    - a collection of radio items
    - an optional radio input locator used as the authoritative state source
    - an optional label locator (inherited) used as the preferred interaction
      target and identity source

    Parameters:
        root:
            Locator tree describing the logical scope of the radio group.
            This may be a form, fieldset, container, or any meaningful grouping
            element.

        items:
            Locator tree describing the collection of radio items.
            Each resolved item represents a logical radio option and serves
            as the relative scope for resolving `input` and `label`.

            Depending on the UI structure, an item may represent:
            - a wrapper element
            - a label element
            - an input element itself

        input:
            Optional locator tree describing the radio input element relative
            to each item.

            When provided, the input element is treated as the **authoritative
            state source** for checked/unchecked evaluation.

            When omitted, the consuming component is expected to fall back to
            evaluating state from the item root itself.

        label:
            Optional locator tree describing the label element relative to each
            item.

            This field is inherited from ButtonBySpec and represents the
            preferred interaction target and text/identity source when present.

            When omitted, the item root may be treated as the interaction and
            identity source.

    Notes:
        - RadioGroupBySpec is a declarative specification only; it performs no
          element resolution, interaction, or state evaluation.
        - No assumptions are made about DOM nesting or element ordering.
        - Interpretation of item, input, and label relationships is entirely
          controlled by locator design and consuming component behavior.
    """

    def __init__(
        self,
        root: LocatorTree,
        items: LocatorTree,
        input: Optional[LocatorTree] = None,
        label: Optional[LocatorTree] = None,
    ):
        super().__init__(root, label)
        self.items = items
        self.input = input
