from typing import Optional, Any

from hyperiontf.ui.widget import Widget
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

    def _eq_map(self) -> dict:
        """
        Build dispatch map for ``__eq__`` comparator handlers.

        Returns:
            dict:
                Mapping of ``type(other).__name__`` to a comparison method.
        """
        return {
            "int": self._eq_int,
            "str": self._eq_str,
            "widget": self._eq_klass,
            "rule": self._eq_rule,
            "dict": self._eq_dict,
        }

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

    def __eq__(self, other) -> bool:
        """
        Compare this rule with a supported selector-like value.

        Dispatches comparison to a typed handler based on ``other`` runtime type.
        Unsupported types are treated as non-equal.
        """
        method = self._eq_map().get(self._get_other_type_str(other), self._eq_false)
        return method(other)

    @staticmethod
    def _get_other_type_str(other: Any) -> str:
        if isinstance(other, SlotPolicyRule):
            return "rule"

        if isinstance(other, Widget):
            return "widget"

        return type(other).__name__

    @staticmethod
    def _eq_false(_other: Any):
        """
        Fallback comparator for unsupported ``other`` types.

        Returns:
            bool:
                Always ``False``.
        """
        return False

    def _eq_int(self, other: int) -> bool:
        """
        Compare by numeric selector value for INDEX rules only.

        Parameters:
            other:
                Integer selector to compare against ``self.value``.
        """
        if self.kind != SlotRuleKind.INDEX:
            return False
        return self.value == other

    def _eq_str(self, other: str) -> bool:
        """
        Compare by string selector value when string matching is allowed.

        Parameters:
            other:
                String selector to compare against ``self.value``.
        """
        if self.kind in [SlotRuleKind.PREDICATE, SlotRuleKind.KEY, SlotRuleKind.EQL]:
            return False

        return self.value == other

    def _eq_klass(self, other: WidgetClassType) -> bool:
        """
        Compare by target widget class identity.

        Parameters:
            other:
                Widget class candidate.
        """
        return self.klass == other

    def _eq_rule(self, other: "SlotPolicyRule") -> bool:
        """
        Compare full rule identity (value, class, and kind).

        Parameters:
            other:
                Another ``SlotPolicyRule`` instance.
        """
        return (
            self.value == other.value
            and self.klass == other.klass
            and self.kind == other.kind
        )

    def _eq_dict(self, other: dict) -> bool:
        """
        Compare by dictionary representation of the rule.

        Parameters:
            other:
                Dictionary containing rule attributes.
        """
        keys = ("value", "kind", "klass")

        any_present = False
        for key in keys:
            if key in other:
                any_present = True
                if getattr(self, key) != other[key]:
                    return False

        return any_present
