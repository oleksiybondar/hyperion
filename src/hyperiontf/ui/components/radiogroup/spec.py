from typing import Optional

from hyperiontf.typing import LocatorTree
from hyperiontf.ui.components.button.spec import ButtonBySpec


class RadioGroupBySpec(ButtonBySpec):
    """
    Specification object for a RadioGroup component.

    RadioGroupBySpec defines the **declarative structure** required to model
    a group of radio options in a backend-agnostic and DOM-agnostic way.

    The specification supports real-world UI variability where:
    - a dedicated item wrapper may or may not exist
    - the radio input may be hidden or not directly clickable
    - the clickable label and the checked state source may be different elements

    A RadioGroup specification consists of:
    - a logical root that scopes the group
    - a collection of radio items
    - an optional input locator (per item) used as the authoritative state node
    - an optional label locator (inherited) used as a preferred interaction/identity node
    - an optional EQL checked expression evaluated against a deterministic target node

    Parameters:
        root:
            Locator tree describing the logical scope of the radio group.
            This may be a form, fieldset, container, or any meaningful grouping element.

        items:
            Locator tree describing the collection of radio items.
            Each resolved item represents a logical radio option and serves
            as the relative scope for resolving `input` and `label`.

            Depending on the UI structure, an item may represent:
            - a wrapper element
            - a label element
            - an input element itself

        input:
            Optional locator tree describing the radio input element relative to each item.

            When provided, the resolved input element is treated as the **authoritative
            target** for checked/unchecked evaluation.

            When omitted, checked-state evaluation falls back to the item root itself.

        label:
            Optional locator tree describing the label element relative to each item.

            This field is inherited from ButtonBySpec and represents the preferred
            interaction target and text/identity source when present.

            When omitted, the item root may be treated as the interaction and identity source.

        checked_expression:
            Optional EQL boolean expression used to determine checked state for custom radios.

            **Evaluation target (important):**
            - If `input` is provided, the expression is evaluated against the resolved *input* node.
            - Otherwise, the expression is evaluated against the resolved *item* node.

            Because of this, do not write expressions that assume an `input` child exists
            (e.g. `input.attribute:...`). If `input` is provided, the expression already runs
            *on* the input node; if `input` is not provided, there is no input node to reference.

            Example (wrapper carries state):
                attribute:aria-checked == true

            Example (input carries state):
                attribute:checked == true

    Notes:
        - RadioGroupBySpec is declarative only; it performs no element resolution, interaction,
          or state evaluation.
        - No assumptions are made about DOM nesting or element ordering.
        - Interpretation of item, input, and label relationships is controlled by locator design
          and consuming component behavior.
    """

    def __init__(
        self,
        root: LocatorTree,
        items: LocatorTree,
        input: Optional[LocatorTree] = None,
        label: Optional[LocatorTree] = None,
        checked_expression: Optional[str] = None,
    ):
        super().__init__(root, label)
        self.items = items
        self.input = input
        self.checked_expression = checked_expression
