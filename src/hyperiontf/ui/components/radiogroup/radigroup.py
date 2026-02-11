import re
from typing import Union, Optional

from hyperiontf.helpers.regexp import verify_semantic_match
from hyperiontf.typing import NoSuchElementException
from hyperiontf.ui.decorators.page_object_helpers import widgets
from hyperiontf.ui.components.radiogroup.radio_item import RadioItem
from hyperiontf.ui.components.base_component import BaseComponent
from hyperiontf.ui.components.helpers.make_eql_selector import make_eql_selector
from hyperiontf.ui.helpers.prepare_expect_object import prepare_expect_object


class Radiogroup(BaseComponent):
    """
    Reusable RadioGroup component.

    ``Radiogroup`` models a logical group of mutually exclusive options using a
    specification-first design (`RadioGroupBySpec`) and reusable `RadioItem` widgets.

    The component is DOM-agnostic and backend-agnostic. All structural knowledge
    comes from the owning Page Object via its component specification:

        - ``root`` defines the logical group scope
        - ``items`` defines the collection of radio options
        - optional ``input`` / ``label`` define per-item structure
        - optional ``checked_expression`` defines custom checked-state evaluation

    Selection strategy
        Items can be selected by:
            - index (int)
            - semantic text (str)
            - regular expression (re.Pattern)

        Text/pattern matching is implemented using EQL selector generation
        via ``make_eql_selector``.

    Checked-state resolution
        The currently selected item is determined by evaluating an EQL predicate
        (`checked_expression`) against the radio item collection.

        - If the spec defines `checked_expression`, it is used.
        - Otherwise, native input semantics are assumed
          (default: ``attribute:checked == true``).

    Collection semantics
        Radio items are collection entities. The item index represents a stable
        position in the resolved collection while that slot exists. Item content
        (text, attributes, state) is always resolved fresh and reflects the
        current DOM at that index.

    Assertion philosophy
        This component provides both:
            - verify_* methods (non-failing decision logging)
            - assert_* methods (failing test assertions)

        Mutual-exclusion invariants are enforced via:
            - assert_none_selected()
            - assert_only_one_selected()
            - assert_at_most_one_selected()
    """

    @widgets(klass=RadioItem)
    def radio_items(self):
        """
        Collection of radio options as `RadioItem` widgets.

        The collection is resolved using `component_spec.items`.
        Individual items can be accessed by index or by EQL selector.
        """
        return self.component_spec.items

    @property
    def checked_expression(self) -> str:
        """
        EQL expression used to identify the selected radio item.

        Returns:
            The spec-defined `checked_expression` if provided,
            otherwise the default native-radio predicate:
            ``attribute:checked == 'true'``.
        """
        if self.component_spec.checked_expression:
            return self.component_spec.checked_expression

        return "attribute:checked == 'true'"

    def select(self, item: Union[int, str, re.Pattern]):
        """
        Select a radio option.

        Args:
            item:
                - int: select by index
                - str: select by semantic text match
                - re.Pattern: select by regex match

        Raises:
            NoSuchElementException:
                If no matching option is found (for text/pattern lookup).
        """
        radio_option = self._find_radio_item(item)
        if not radio_option:
            raise NoSuchElementException(f"There is no item: {item}")

        radio_option.click()

    def has_item(self, item: Union[str, re.Pattern]) -> bool:
        """
        Return True if an item matching the given text/pattern exists.

        This is a non-asserting presence check intended for control flow.
        """
        return self.radio_items[make_eql_selector(item)] is not None

    def _find_radio_item(self, item: Union[int, str, re.Pattern]):
        """
        Internal resolver for radio items.

        - int resolves via collection indexing
        - str / re.Pattern resolves via EQL selector

        Returns:
            A `RadioItem` if found, otherwise None (for selector-based lookup).
        """
        if isinstance(item, int):
            return self.radio_items[item]

        return self.radio_items[make_eql_selector(item)]

    @property
    def selected_item(self) -> Optional[RadioItem]:
        """
        Return the currently selected radio item.

        The selected item is determined by applying `checked_expression`
        against the radio item collection.

        Returns:
            A `RadioItem` if one matches the predicate,
            otherwise None.
        """
        return self.radio_items[self.checked_expression]

    @property
    def selected_item_text(self) -> Optional[str]:
        """
        Return the text/identity of the currently selected item.

        Text resolution is delegated to `RadioItem.get_text()`, which may read
        from a label element (if defined) or from the item root.
        """
        item = self.selected_item
        if item:
            return item.get_text()

        return None

    @property
    def selected_item_index(self) -> Optional[int]:
        """
        Return the index of the currently selected item.

        The index is derived from the internal collection locator metadata
        (`LocatorStrategies.ELEMENTS_ITEM`). It represents the position
        of the item in the collection.

        Stability contract:
            - If the item at that position still exists, the index remains stable.
            - The item's content is always resolved fresh from the DOM.

        Returns:
            int index if an item is selected, otherwise None.
        """
        item = self.selected_item
        if item:
            return int(getattr(item, "_locator").value)

        return None

    def verify_selected_value(self, expected: Union[str, re.Pattern]):
        """
        Verify that the currently selected item's text matches the expected value.

        Non-failing check intended for decision logging.
        """
        actual_value = self.selected_item_text
        verify = prepare_expect_object(
            self,
            actual_value,
            False,
            "Verifying currently selected value",
            self._logger,
        )
        return verify_semantic_match(verify, expected)

    def assert_selected_value(self, expected: Union[str, re.Pattern]):
        """
        Assert that the currently selected item's text matches the expected value.
        """
        actual_value = self.selected_item_text
        verify = prepare_expect_object(
            self,
            actual_value,
            True,
            "Asserting currently selected value",
            self._logger,
        )
        return verify_semantic_match(verify, expected)

    def assert_selected_index(self, expected: int):
        """
        Assert that the currently selected item's index matches the expected index.
        """
        index = self.selected_item_index
        verify = prepare_expect_object(
            self,
            index,
            True,
            "Asserting currently selected value by index",
            self._logger,
        )
        return verify.to_be(expected)

    def verify_has_item(self, item: Union[str, re.Pattern]):
        """
        Verify that an item matching the given text/pattern exists.
        """
        radio_item = self._find_radio_item(item)
        verify = prepare_expect_object(
            self,
            radio_item,
            False,
            f'Verifying item "{item}" presents',
            self._logger,
        )
        return verify.is_not_none()

    def verify_item_missing(self, item: Union[str, re.Pattern]):
        """
        Verify that an item matching the given text/pattern does not exist.
        """
        radio_item = self._find_radio_item(item)
        verify = prepare_expect_object(
            self,
            radio_item,
            False,
            f'Verifying item "{item}" absents',
            self._logger,
        )
        return verify.is_none()

    def assert_has_item(self, item: Union[str, re.Pattern]):
        """
        Assert that an item matching the given text/pattern exists.
        """
        radio_item = self._find_radio_item(item)
        verify = prepare_expect_object(
            self,
            radio_item,
            True,
            f'Asserting item "{item}" presents',
            self._logger,
        )
        return verify.is_not_none()

    def assert_item_missing(self, item: Union[str, re.Pattern]):
        """
        Assert that an item matching the given text/pattern does not exist.
        """
        radio_item = self._find_radio_item(item)
        verify = prepare_expect_object(
            self,
            radio_item,
            True,
            f'Assertion item "{item}" absents',
            self._logger,
        )
        return verify.is_none()

    def assert_radio_state(
        self, selected: Optional[Union[int, str, re.Pattern]] = None
    ):
        """
        Assert high-level RadioGroup invariants.

        If `selected` is provided:
            - int → assert selected index
            - str / Pattern → assert selected value

        Then asserts that the group satisfies the mutual-exclusion invariant
        (at most one selected).
        """
        if selected is not None:
            if isinstance(selected, int):
                self.assert_selected_index(selected)
            else:
                self.assert_selected_value(selected)

        self.assert_at_most_one_selected()

    def assert_none_selected(self):
        """
        Assert that no radio option is currently selected.
        """
        selected = self.radio_items.select_all(self.checked_expression)
        verify = prepare_expect_object(
            self,
            selected,
            True,
            "Asserting that no options is currently selected value",
            self._logger,
        )
        return verify.to_have_length(0)

    def assert_only_one_selected(self):
        """
        Assert that exactly one radio option is currently selected.
        """
        selected = self.radio_items.select_all(self.checked_expression)
        verify = prepare_expect_object(
            self,
            selected,
            True,
            "Asserting that only one is currently selected value",
            self._logger,
        )
        return verify.to_have_length(1)

    def assert_at_most_one_selected(self):
        """
        Assert that zero or one radio options are currently selected.

        This enforces the mutual-exclusion invariant of a radio group
        without requiring that a selection must exist.
        """
        selected = self.radio_items.select_all(self.checked_expression)
        verify = prepare_expect_object(
            self,
            len(selected),
            True,
            "Asserting that none or one is currently selected value",
            self._logger,
        )
        return verify.to_be_less_than_or_equal_to(1)
