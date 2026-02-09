import re
from typing import Optional, Union

from hyperiontf.typing import NoSuchElementException
from hyperiontf.ui.components.button.button import Button
from hyperiontf.ui.decorators.page_object_helpers import elements
from hyperiontf.ui.helpers.prepare_expect_object import prepare_expect_object
from hyperiontf.helpers.regexp import is_regex, regexp_to_eql


class Dropdown(Button):
    """
    Interactive Dropdown component.

    Dropdown represents a selectable UI control composed of:
    - a clickable trigger (inherited from Button)
    - a dynamically rendered collection of option elements

    The component supports dropdown implementations where options may be
    rendered outside the trigger hierarchy (e.g. overlays, portals, or
    document-level menus).

    Selection supports multiple strategies:
    - index-based
    - exact text match (via EQL text equality)
    - regular-expression match (via EQL pattern)

    Dropdown inherits trigger/label behavior from Button and extends it
    with option discovery, selection, selected-value resolution, and
    assertion/verification helpers.
    """

    @elements
    def dropdown_options(self):
        """
        Return the collection of dropdown option elements.

        Options are resolved using the locator defined in the associated
        DropdownBySpec. The returned collection may represent elements
        rendered outside the trigger hierarchy (e.g. sibling menus, portals).

        Returns:
            Elements:
                Collection representing the currently resolvable options.
                Presence/visibility depends on the dropdown being open and on
                the UI implementation (some dropdowns render options only
                while opened).
        """
        return self.component_spec.options

    @property
    def are_options_opened(self) -> bool:
        """
        Determine whether dropdown options are currently rendered and visible.

        This is a best-effort heuristic:
        - options must be present
        - the first option must be visible

        Returns:
            bool:
                True if options are present and at least one option is visible,
                False otherwise.
        """
        return self.dropdown_options.is_present and self.dropdown_options[0].is_visible

    def open_dropdown(self) -> None:
        """
        Open the dropdown if it is not already open.

        This method is idempotent and safe to call multiple times.

        Notes:
            Some UI implementations render options only when opened. This
            method is used as a prerequisite for option discovery.
        """
        if not self.are_options_opened:
            self.click()

    def close_dropdown(self) -> None:
        """
        Close the dropdown if it is currently open.

        This method is idempotent and safe to call multiple times.
        """
        if self.are_options_opened:
            self.click()

    def select(self, option: Union[int, str, re.Pattern]) -> None:
        """
        Select a dropdown option.

        Selection strategies:
        - int: select option by index
        - str: select option by exact visible text match (via EQL)
        - re.Pattern: select option whose visible text matches the pattern (via EQL)

        Parameters:
            option:
                Option selector expression.

        Raises:
            NoSuchElementException:
                If no matching option is found.

        Notes:
            The dropdown is opened to discover options. Closing behavior after
            selection is UI-dependent (many dropdowns close automatically when
            an option is clicked).
        """
        dd_option = self._open_and_find_option(option)
        if not dd_option:
            raise NoSuchElementException(f"There is no option: {option}")

        dd_option.click()

    def _find_option(self, expression: Union[int, str, re.Pattern]):
        """
        Resolve a dropdown option using the provided selector expression.

        Parameters:
            expression:
                Index, exact text, or regex-based selector.

        Returns:
            Element | None:
                The resolved option element, or None if not found.
        """
        if isinstance(expression, int):
            return self._find_by_index(expression)
        return self._find_by_eql(expression)

    def _find_by_index(self, index: int):
        """
        Resolve a dropdown option by index.

        Parameters:
            index:
                Zero-based option index.

        Returns:
            Element:
                The option element at the specified index.

        Notes:
            Indexing semantics are provided by the underlying Elements collection.
        """
        return self.dropdown_options[index]

    def _find_by_eql(self, expression: Union[str, re.Pattern]):
        """
        Resolve a dropdown option using an EQL selector.

        Parameters:
            expression:
                Exact text (str) or a compiled regular expression.

        Returns:
            Element | None:
                The first matching option element, or None if not found.
        """
        eql = self._expression_to_eql(expression)
        return self.dropdown_options[eql]

    @staticmethod
    def _expression_to_eql(expression: Union[str, re.Pattern]) -> str:
        """
        Convert a string or compiled regex into an EQL selector.

        Parameters:
            expression:
                A string for exact match, or a compiled regex pattern.

        Returns:
            str:
                EQL selector string.
        """
        if is_regex(expression):
            return f"text ~= {regexp_to_eql(expression)}"
        return f'text == "{expression}"'

    @property
    def selected_value(self) -> Optional[str]:
        """
        Return the currently selected value as resolved by the dropdown.

        This property resolves the selected value using the strategy configured
        by `DropdownBySpec.value_attribute`.

        Returns:
            Optional[str]:
                The resolved selected value. The value may be empty or None-like
                depending on the underlying control and its current state.
        """
        return self._get_selected_value(log=True)

    @property
    def selected_option_index(self) -> Optional[int]:
        """
        Return the index of the currently selected option, if resolvable.

        The dropdown is opened temporarily to ensure options are rendered
        (important for decoupled/portal dropdowns).

        Resolution model:
        - resolve the current selected value (see `selected_value`)
        - locate the matching option in `dropdown_options`
        - return its index

        Returns:
            Optional[int]:
                Index of the selected option, or None if no matching option can
                be determined (e.g. placeholder state or unmatched value).
        """
        selected_option = self._get_option(self._get_selected_value())
        if selected_option:
            return int(getattr(selected_option, "_locator").value)
        return None

    def verify_selected_value(self, expected):
        """
        Verify that the currently selected value matches the expected value.

        This is a non-fatal check and returns an expectation object.

        Parameters:
            expected:
                Expected selected value.

        Returns:
            Expectation:
                Non-fatal expectation result (does not fail the test).
        """
        actual_value = self._get_selected_value()
        verify = prepare_expect_object(
            self,
            actual_value,
            False,
            "Verifying currently selected value",
            self._logger,
        )
        return verify.to_be(expected)

    def assert_selected_value(self, expected):
        """
        Assert that the currently selected value matches the expected value.

        This is a fatal assertion and will fail the test if the value does not match.

        Parameters:
            expected:
                Expected selected value.

        Returns:
            Expectation:
                Fatal expectation result (fails the test on mismatch).
        """
        actual_value = self._get_selected_value()
        verify = prepare_expect_object(
            self,
            actual_value,
            True,
            "Asserting currently selected value",
            self._logger,
        )
        return verify.to_be(expected)

    def _get_option(self, expression: Union[str, re.Pattern]):
        """
        Open the dropdown, resolve an option, then close the dropdown.

        Parameters:
            expression:
                Option selector expression (text or regex).

        Returns:
            Element | None:
                The resolved option element, or None if not found.
        """
        dd_option = self._open_and_find_option(expression)
        self.close_dropdown()
        return dd_option

    def _open_and_find_option(self, expression: Union[int, str, re.Pattern]):
        """
        Open the dropdown and resolve an option without closing it.

        Parameters:
            expression:
                Option selector expression.

        Returns:
            Element | None:
                The resolved option element, or None if not found.
        """
        self.open_dropdown()
        return self._find_option(expression)

    def verify_has_option(self, option: Union[str, re.Pattern]):
        """
        Verify that the dropdown contains the specified option.

        This is a non-fatal verification.

        Parameters:
            option:
                Option text or regex pattern.

        Returns:
            Expectation:
                Non-fatal expectation result.
        """
        dd_option = self._get_option(option)
        verify = prepare_expect_object(
            self,
            dd_option,
            False,
            f'Verifying option "{option}" presents',
            self._logger,
        )
        return verify.is_not_none()

    def verify_option_missing(self, option: Union[str, re.Pattern]):
        """
        Verify that the dropdown does not contain the specified option.

        This is a non-fatal verification.

        Parameters:
            option:
                Option text or regex pattern.

        Returns:
            Expectation:
                Non-fatal expectation result.
        """
        dd_option = self._get_option(option)
        verify = prepare_expect_object(
            self,
            dd_option,
            False,
            f'Verifying option "{option}" absents',
            self._logger,
        )
        return verify.is_none()

    def assert_has_option(self, option: Union[str, re.Pattern]):
        """
        Assert that the dropdown contains the specified option.

        This is a fatal assertion.

        Parameters:
            option:
                Option text or regex pattern.

        Returns:
            Expectation:
                Fatal expectation result.
        """
        dd_option = self._get_option(option)
        verify = prepare_expect_object(
            self,
            dd_option,
            True,
            f'Asserting option "{option}" presents',
            self._logger,
        )
        return verify.is_not_none()

    def assert_option_missing(self, option: Union[str, re.Pattern]):
        """
        Assert that the dropdown does not contain the specified option.

        This is a fatal assertion.

        Parameters:
            option:
                Option text or regex pattern.

        Returns:
            Expectation:
                Fatal expectation result.
        """
        dd_option = self._get_option(option)
        verify = prepare_expect_object(
            self,
            dd_option,
            True,
            f'Assertion option "{option}" absents',
            self._logger,
        )
        return verify.is_none()

    def _get_selected_value(self, log: bool = False) -> str:
        """
        Resolve the currently selected value using the configured value strategy.

        The strategy is controlled by `DropdownBySpec.value_attribute`:

        - "AUTO":
            Use heuristic resolution based on the underlying control type.
        - "text" or None:
            Resolve selected value via visible text (trigger/label text).
        - any other string:
            Treat it as a DOM attribute name and resolve selected value via
            `get_attribute(<name>)`.

        Parameters:
            log:
                Whether to include the resolution call in logging.

        Returns:
            str:
                Resolved selected value string.
        """
        if self.component_spec.value_attribute == "AUTO":
            return self._auto_resolve_selected_value(log=log)
        if self.component_spec.value_attribute in ["text", None]:
            return self.get_text(log=log)
        return self.get_attribute(self.component_spec.value_attribute, log=log)

    def _auto_resolve_selected_value(self, log: bool = False) -> str:
        """
        Resolve selected value using heuristic rules.

        Heuristic behavior:
        - For native input/select-like controls, prefer attribute-based value
          resolution via the "value" attribute.
        - For custom dropdowns (typical JS menus), prefer visible text via
          `get_text()`.

        Parameters:
            log:
                Whether to include the resolution call in logging.

        Returns:
            str:
                Resolved selected value string.
        """
        element_tag = self.get_attribute("tagName", log=True).lower()
        if element_tag in ["select", "input"]:
            return self.get_attribute("value", log=log)
        return self.get_text(log=log)
