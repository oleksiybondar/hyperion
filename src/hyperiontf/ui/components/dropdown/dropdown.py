import re
from typing import Optional, Union

from hyperiontf.typing import NoSuchElementException
from hyperiontf.ui.components.button.button import Button
from hyperiontf.ui.decorators.page_object_helpers import elements
from hyperiontf.ui.helpers.prepare_expect_object import prepare_expect_object


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
    - exact text match
    - regular-expression match (via EQL)

    Dropdown inherits trigger/label behavior from Button and extends it
    with option discovery, selection, and verification semantics.
    """

    @elements
    def dropdown_options(self):
        """
        Return the collection of dropdown option elements.

        Options are resolved using the locator defined in the associated
        DropdownBySpec. The returned collection may represent elements
        rendered outside the trigger hierarchy.

        Returns:
            Elements collection representing the currently rendered options.
        """
        return self.component_spec.options

    @property
    def are_options_opened(self) -> bool:
        """
        Determine whether dropdown options are currently rendered and visible.

        Returns:
            True if options are present and at least one option is visible,
            False otherwise.
        """
        return self.dropdown_options.is_present and self.dropdown_options[0].is_visible

    def open_dropdown(self) -> None:
        """
        Open the dropdown if it is not already open.

        This method is idempotent and safe to call multiple times.
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
        - str: select option with exact text match
        - re.Pattern: select option whose text matches the pattern

        Parameters:
            option:
                Option selector expression.

        Raises:
            NoSuchElementException:
                If no matching option is found.
        """
        self.open_dropdown()
        dd_option = self._find_option(option)
        if not dd_option:
            raise NoSuchElementException(f"There is no option: {option}")

        dd_option.click()

    def _find_option(self, expression: Union[int, str, re.Pattern]):
        """
        Resolve a dropdown option using the provided selector expression.

        Parameters:
            expression:
                Index, text, or regex-based selector.

        Returns:
            The resolved option element, or None if not found.
        """
        if isinstance(expression, int):
            return self._find_by_index(expression)
        else:
            return self._find_by_eql(expression)

    def _find_by_index(self, index: int):
        """
        Resolve a dropdown option by index.

        Parameters:
            index:
                Zero-based option index.

        Returns:
            The option element at the specified index.
        """
        return self.dropdown_options[index]

    def _find_by_eql(self, expression: Union[str, re.Pattern]):
        """
        Resolve a dropdown option using an EQL expression.

        Parameters:
            expression:
                Exact text or regular expression.

        Returns:
            The first matching option element, or None if not found.
        """
        eql = self._expression_to_eql(expression)
        return self.dropdown_options[eql]

    @staticmethod
    def _expression_to_eql(expression: Union[str, re.Pattern]) -> str:
        """
        Convert a string or regex expression into an EQL selector.

        Parameters:
            expression:
                String or compiled regular expression.

        Returns:
            EQL selector string.
        """
        if isinstance(expression, re.Pattern):
            return f"text ~= /{expression}/"

        return f'text == "{expression}"'

    @property
    def selected_option_index(self) -> Optional[int]:
        """
        Return the index of the currently selected option, if resolvable.

        The dropdown is opened temporarily to ensure options are rendered
        (important for decoupled or portal-based dropdowns).

        Returns:
            Index of the selected option, or None if no match is found.
        """
        selected_option = self._get_option(self.get_text(log=False))
        if selected_option:
            return selected_option.index
        return None

    def verify_selected_value(self, expected):
        """
        Verify that the currently selected value matches the expected value.

        This is a non-fatal check and returns an expectation object.
        """
        return self.verify_text(expected)

    def assert_selected_value(self, expected):
        """
        Assert that the currently selected value matches the expected value.

        This is a fatal assertion and will fail the test if the value
        does not match.
        """
        return self.assert_text(expected)

    def _get_option(self, expression: Union[str, re.Pattern]):
        """
        Open the dropdown, resolve an option, then close the dropdown.

        Parameters:
            expression:
                Option selector expression.

        Returns:
            The resolved option element, or None if not found.
        """
        dd_option = self._open_and_find_option(expression)
        self.close_dropdown()
        return dd_option

    def _open_and_find_option(self, expression: Union[str, re.Pattern]):
        """
        Open the dropdown and resolve an option without closing it.

        Parameters:
            expression:
                Option selector expression.

        Returns:
            The resolved option element, or None if not found.
        """
        self.open_dropdown()
        return self._find_option(expression)

    def verify_has_option(self, option: Union[str, re.Pattern]):
        """
        Verify that the dropdown contains the specified option.

        This is a non-fatal verification.
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
        """
        dd_option = self._get_option(option)
        verify = prepare_expect_object(
            self, dd_option, False, f'Verifying option "{option}" absents', self._logger
        )
        return verify.is_none()

    def assert_has_option(self, option: Union[str, re.Pattern]):
        """
        Assert that the dropdown contains the specified option.

        This is a fatal assertion.
        """
        dd_option = self._get_option(option)
        verify = prepare_expect_object(
            self, dd_option, True, f'Asserting option "{option}" presents', self._logger
        )
        return verify.is_not_none()

    def assert_option_missing(self, option: Union[str, re.Pattern]):
        """
        Assert that the dropdown does not contain the specified option.

        This is a fatal assertion.
        """
        dd_option = self._get_option(option)
        verify = prepare_expect_object(
            self, dd_option, True, f'Assertion option "{option}" absents', self._logger
        )
        return verify.is_none()
