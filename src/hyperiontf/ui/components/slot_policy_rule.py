from typing import Optional

from hyperiontf.ui.components.typing import SlotRuleKindType, SlotRuleKind
from hyperiontf.ui.components.typing import (
    WidgetClassType,
    SlotSelectorType,
    SlotPredicate,
)


class SlotPolicyRule:
    """
    Represents a single rule used by a slot policy to determine how a logical slot
    (e.g. a table cell, tab panel, or dialog section) should be materialized.

    A SlotPolicyRule binds:
    - a selector value (index, key, or predicate keyword)
    - to a target widget class

    The rule's *kind* determines how the selector value is interpreted.

    Parameters:
        value:
            Selector value used to match a slot.

            Supported forms:
            - int:
                Interpreted as an index selector (supports negative indices, e.g. -1 for last).
            - str:
                Interpreted either as:
                - a predicate keyword (e.g. "ALL", "LAST"), or
                - a context-defined key (e.g. column name),
                depending on inference rules or explicit kind.

        klass:
            Widget class to materialize when this rule matches.
            If no rule matches, default materialization is handled by the consumer
            (typically a plain Element).

        kind:
            Optional explicit rule kind.

            If not provided, the kind is inferred deterministically:
            - int value       -> INDEX
            - str value in SlotPredicate -> PREDICATE
            - other str       -> KEY

            The EQL rule kind is **never inferred automatically** and must be
            explicitly provided when required.

    Notes:
        - SlotPolicyRule is a value object; it does not perform rule evaluation.
        - Rule ordering and precedence ("last match wins") are defined by the
          consuming component via policy-by-ordering.
        - EQL-based rules must be explicitly declared using kind=SlotRuleKind.EQL.
    """

    def __init__(
        self,
        value: SlotSelectorType,
        klass: WidgetClassType,
        kind: Optional[SlotRuleKindType] = None,
    ):
        self.value = value
        self.klass = klass
        self.kind: SlotRuleKindType = kind or self._resolve_kind()

    def _resolve_kind(self) -> SlotRuleKindType:
        """
        Infer the rule kind from the selector value when no explicit kind is provided.

        Inference rules:
        - int value       -> INDEX
        - str value in SlotPredicate -> PREDICATE
        - other str       -> KEY

        EQL rules are intentionally excluded from inference and must be
        explicitly declared by the caller.
        """
        if isinstance(self.value, int):
            return SlotRuleKind.INDEX

        if self._value_is_predicate():
            return SlotRuleKind.PREDICATE

        return SlotRuleKind.KEY

    def _value_is_predicate(self) -> bool:
        """
        Determine whether the selector value matches a reserved predicate keyword.

        Returns:
            True if the value is one of the predefined SlotPredicate values,
            False otherwise.

        Notes:
            Predicate keywords have fixed semantics and are distinct from
            key-based selectors. This check is used only during kind inference.
        """
        predicates = [value for value in vars(SlotPredicate).values()]
        return self.value in predicates
