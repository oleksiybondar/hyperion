from typing import Final, Literal, Sequence, Type, TypeAlias, Union, TypeVar

from hyperiontf.ui.widget import Widget

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Slot Policy Section
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

SlotRuleKindType = Literal["index", "predicate", "key", "eql"]


class SlotRuleKind:
    """
    Defines the kind of selector used by a SlotPolicyRule.

    SlotRuleKind determines *how* the rule's value is interpreted when resolving
    a logical slot (for example, a table cell or tab panel).

    Supported kinds:

    - INDEX:
        The value is an integer index applied to an ordered structure.
        Negative indices are supported (e.g. -1 for last).

    - PREDICATE:
        The value is a reserved keyword with predefined meaning
        (e.g. "ALL", "LAST"). Predicate semantics are fixed and deterministic.

    - KEY:
        The value is a context-defined string key.
        Interpretation depends on the owning component (e.g. column key in a table).

    - EQL:
        The value is an Element Query Language (EQL) expression.
        EQL rules are **never inferred automatically** and must be explicitly declared.
        They allow advanced, internal matching logic such as resolving an index
        from a string expression in the Hyperion domain.

    Notes:
        - Rule kinds control interpretation only; evaluation semantics
          (ordering, precedence, matching) are defined by the consuming component.
        - Slot policy rules are evaluated using a policy-by-ordering model
          (last matching rule wins).
    """

    INDEX: SlotRuleKindType = "index"
    PREDICATE: SlotRuleKindType = "predicate"
    KEY: SlotRuleKindType = "key"
    EQL: SlotRuleKindType = "eql"


SlotPredicateType = Literal[
    "ALL",
    "LAST",
    "FIRST",
]


class SlotPredicate:
    """
    Reserved slot predicate keywords.

    These keywords are used by slot policy rule inference to deterministically
    distinguish predicates from key-based selectors.

    Note:
        - If a string selector equals one of these keywords, it is treated as a predicate
          unless the rule kind is explicitly provided.
        - Ordering semantics are defined by the consumer (policy-by-ordering / last match wins).
    """

    ALL: SlotPredicateType = "ALL"
    LAST: SlotPredicateType = "LAST"
    FIRST: SlotPredicateType = "FIRST"


RESERVED_SLOT_PREDICATES: Final[frozenset[str]] = frozenset(
    {
        SlotPredicate.ALL,
        SlotPredicate.LAST,
        SlotPredicate.FIRST,
    }
)

# A selector value used in SlotPolicyRule:
# - int: index selector (supports negative, e.g. -1 for last)
# - str: predicate keyword (reserved) or key selector (context-defined)
SlotSelectorType: TypeAlias = Union[int, str]

# Widget class type used for materialization (Element is implied by default behavior elsewhere).
WidgetClassType: TypeAlias = Type[Widget]

# Public slot policy type: an ordered list of rules (policy-by-ordering; last match wins).
# Forward-referenced to avoid import cycles with the rule implementation module.
SlotPolicyRule = TypeVar("SlotPolicyRule")
SlotPolicyType: TypeAlias = Sequence[SlotPolicyRule]
