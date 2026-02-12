from typing import List, Optional, Callable, cast

from hyperiontf.ui.components.typing import (
    SlotPredicate,
    SlotRuleKind,
    SlotPredicateType,
)
from hyperiontf.ui.element import Element
from hyperiontf.ui.eql.executor import evaluate
from hyperiontf.ui.eql.parser import parse
from hyperiontf.ui.widget import Widget

from hyperiontf.ui.components.slot_policy_rule import SlotPolicyRule


class SlotRuleResolver:
    """
    Resolves the concrete widget class for a logical slot by applying ordered slot policy rules.

    SlotRuleResolver evaluates a list of :class:`~hyperiontf.ui.components.slot_policy_rule.SlotPolicyRule`
    against an (index, element) pair within an ordered structure (e.g. table cells, tab panels, list items).

    Resolution model
    ----------------
    Rules are applied sequentially in the order they are provided. If multiple rules match the same slot,
    **the last matching rule wins** (policy-by-ordering). The resolver returns the selected widget class
    (typically a subclass of :class:`~hyperiontf.ui.widget.Widget`), or ``None`` if no rule matches.

    Rule kinds
    ----------
    The rule's ``kind`` determines how the rule's ``value`` is interpreted:

    - ``PREDICATE``: Uses reserved keywords such as ``ALL``, ``FIRST``, ``LAST``.
    - ``INDEX``: Matches by numeric index (supports negative indices, e.g. ``-1`` for last).
    - ``EQL``: Matches by evaluating an Element Query Language expression against the element.
    - ``KEY``: Matches by resolving a component-specific key to an index via ``key_to_index_resolver``.

    Component-specific key resolution
    ---------------------------------
    ``KEY`` rules cannot be resolved generically because the meaning of a key depends on the owning
    component (e.g. table column key, tab label). Provide ``key_to_index_resolver`` to translate
    rule keys into indices.

    Parameters
    ----------
    slot_policies:
        Ordered list of slot policy rules. Ordering defines precedence (last match wins).
    key_to_index_resolver:
        Optional callback used for ``KEY`` rules. It is expected to accept the rule's key value
        and return the corresponding integer index for the current component context.
    """

    def __init__(
        self,
        slot_policies: Optional[List[SlotPolicyRule]] = None,
        key_to_index_resolver: Optional[Callable] = None,
    ):
        if slot_policies is None:
            slot_policies = []
        self.slot_policies = slot_policies
        self.key_to_index_resolver = key_to_index_resolver
        self._init_dispatch_map()

    def _init_dispatch_map(self) -> None:
        """
        Initialize the internal dispatch table mapping rule kinds to resolver methods.

        This makes supported kinds explicit and avoids fragile dynamic getattr-based dispatch.
        """
        self._dispatch = {
            SlotRuleKind.PREDICATE: self.resolve_predicate,
            SlotRuleKind.INDEX: self.resolve_index,
            SlotRuleKind.EQL: self.resolve_eql,
            SlotRuleKind.KEY: self.resolve_key,
        }

    def resolve(
        self, index: int, element: Element, total_count: int
    ) -> Optional[Callable[..., Widget]]:
        """
        Resolve the widget class for a slot at a given position.

        Iterates over configured ``slot_policies`` and applies each rule to the provided slot context.
        If a rule matches, its ``klass`` becomes the current result. After all rules are processed,
        the **last matching rule** determines the final returned class.

        Parameters
        ----------
        index:
            Zero-based position of the slot in the ordered structure.
        element:
            The underlying UI element corresponding to the slot at ``index``.
        total_count:
            Total number of items in the ordered structure (used for negative indices and LAST predicate).

        Returns
        -------
        Optional[Callable[..., Widget]]:
            The selected widget class/constructor for the slot, or ``None`` if no rules match.

        Notes
        -----
        - Resolution is "policy-by-ordering": later rules override earlier ones.
        - Unknown rule kinds will raise ``KeyError`` when indexing the internal dispatch map.
        """
        klass = None
        for rule in self.slot_policies:
            method = self._dispatch.get(rule.kind, None)
            if method is None:
                return None
            result = method(rule, index, element, total_count)
            if result is not None:
                klass = result

        return klass

    @staticmethod
    def resolve_predicate(
        rule: SlotPolicyRule, index: int, _element: Element, total_count: int
    ):
        """
        Resolve a predicate-based rule.

        Supported predicates:
        - ``ALL``: Always matches.
        - ``FIRST``: Matches when ``index == 0``.
        - ``LAST``: Matches when ``index == total_count - 1``.

        Parameters
        ----------
        rule:
            Slot policy rule of kind ``PREDICATE``.
        index:
            Slot index.
        _element:
            Unused for predicate resolution.
        total_count:
            Total number of slots in the structure.

        Returns
        -------
        Optional[type]:
            ``rule.klass`` if the predicate matches, otherwise ``None``.
        """
        if rule.value == SlotPredicate.ALL:
            return rule.klass

        predicate_index = {
            SlotPredicate.FIRST: 0,
            SlotPredicate.LAST: total_count - 1,
        }.get(cast(SlotPredicateType, rule.value))

        return (
            rule.klass
            if predicate_index is not None and index == predicate_index
            else None
        )

    @staticmethod
    def resolve_index(
        rule: SlotPolicyRule, index: int, _element: Element, total_count: int
    ):
        """
        Resolve an index-based rule.

        Matches the rule when:
        - ``rule.value`` is a non-negative integer equal to ``index``, or
        - ``rule.value`` is negative and refers to an index from the end
          (e.g. ``-1`` matches the last item, ``-2`` the second-to-last).

        Parameters
        ----------
        rule:
            Slot policy rule of kind ``INDEX``.
        index:
            Slot index.
        _element:
            Unused for index resolution.
        total_count:
            Total number of slots in the structure.

        Returns
        -------
        Optional[type]:
            ``rule.klass`` if the index matches, otherwise ``None``.
        """
        if int(rule.value) < 0:
            match = total_count + int(rule.value) == index
        else:
            match = index == rule.value

        if match:
            return rule.klass

        return None

    @staticmethod
    def resolve_eql(
        rule: SlotPolicyRule, _index: int, element: Element, _total_count: int
    ):
        """
        Resolve an EQL (Element Query Language) rule.

        The rule's EQL expression is parsed and then evaluated against the provided element.
        If the expression evaluates to True, the rule matches.

        Parameters
        ----------
        rule:
            Slot policy rule of kind ``EQL``. The rule's ``value`` is expected to be an EQL expression.
        _index:
            Unused for EQL resolution.
        element:
            Element to evaluate the EQL expression against.
        _total_count:
            Unused for EQL resolution.

        Returns
        -------
        Optional[type]:
            ``rule.klass`` if the EQL expression matches, otherwise ``None``.

        Notes
        -----
        Consider caching parsed EQL queries per rule if performance becomes an issue, since parsing is
        performed each time this resolver is called.
        """
        parsed_query = parse(str(rule.value))
        if evaluate(parsed_query, element):
            return rule.klass

        return None

    def resolve_key(
        self, rule: SlotPolicyRule, index: int, _element: Element, _total_count: int
    ):
        """
        Resolve a key-based rule using a component-provided key-to-index resolver.

        ``KEY`` rules are component-specific: the meaning of ``rule.value`` depends on the owning
        component. For example, a table may map keys via header cell text, while tabs may map keys
        via the tab label.

        Parameters
        ----------
        rule:
            Slot policy rule of kind ``KEY``. The rule's ``value`` is treated as a component-defined key.
        index:
            Slot index to compare against the resolved key index.
        _element:
            Unused for key resolution.
        _total_count:
            Unused for key resolution.

        Returns
        -------
        Optional[type]:
            ``rule.klass`` if the resolved key index equals ``index``, otherwise ``None``.

        Notes
        -----
        - If ``key_to_index_resolver`` is not provided, KEY rules never match.
        """
        if self.key_to_index_resolver is None:
            return None

        resolved_index = self.key_to_index_resolver(rule.value)

        if resolved_index == index:
            return rule.klass

        return None
