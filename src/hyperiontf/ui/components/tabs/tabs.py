import re
from typing import Optional, List, Union

from hyperiontf.typing import NoSuchElementException
from hyperiontf.ui.components.base_component import BaseComponent
from hyperiontf.ui.components.decorators.components import components
from hyperiontf.ui.components.helpers.make_eql_selector import make_eql_selector
from hyperiontf.ui.components.slot_rule_resolver import SlotRuleResolver
from hyperiontf.ui.components.decorators.slots import slots
from hyperiontf.ui.components.button.button import Button
from hyperiontf.ui.components.button.spec import ButtonBySpec
from hyperiontf.ui.helpers.prepare_expect_object import prepare_expect_object


class Tabs(BaseComponent):
    """
    Reusable Tabs component with panel-slot materialization.

    ``Tabs`` models:
    - a collection of tab buttons (`tabs`)
    - a collection of tab panels (`panels`)
    - an active-tab pointer (`selected_tab_index`) used for non-shared panels

    The component supports two panel layouts defined by `TabsBySpec.use_shared_panel`:
    - shared panel: a single panel root reused for all tabs
    - per-tab panels: one panel per tab index

    Tab resolution supports:
    - index-based lookup (`int`)
    - exact text lookup (`str`, via EQL selector)
    - regex lookup (`re.Pattern`, via EQL selector)

    Slot materialization for panel internals is delegated to `SlotRuleResolver`,
    where key-based rules can resolve tab names to indexes via
    `tab_name_to_index_resolver`.
    """

    def __init__(self, parent, locator, name: str):
        """
        Create a Tabs component instance.

        Parameters:
            parent:
                Owning container (Page/Widget/Component).
            locator:
                Component root locator (framework-internal wrapper).
            name:
                Logical name of the component in the Page Object.
        """
        super().__init__(parent, locator, name)
        self._tabs_names: List[str] = []
        self.selected_tab_index = 0
        self.slot_resolver = SlotRuleResolver(
            self.component_spec.slot_policies,
            self.tab_name_to_index_resolver,
        )

    @property
    def has_shared_panel(self) -> bool:
        """Return True when this tabs spec uses a single shared panel root."""
        return self.component_spec.use_shared_panel

    @property
    def tabs_names(self) -> List[str]:
        """
        Return cached tab names resolved from tab button visible text.

        Names are lazily computed from the current `tabs` collection and cached
        until `force_refresh()` is called.
        """
        if len(self._tabs_names) == 0:
            self._tabs_names = [tab.get_text() for tab in self.tabs]
        return self._tabs_names

    def tab_name_to_index_resolver(self, name) -> Optional[int]:
        """
        Resolve a tab name to its index in the current tabs collection.

        Parameters:
            name:
                Visible tab name.

        Returns:
            Optional[int]:
                The resolved index if present, otherwise `None`.
        """
        try:
            return self.tabs_names.index(name)
        except ValueError:
            return None

    @property
    def selected_tab_name(self) -> str:
        """Return the currently tracked selected tab name."""
        return self.tabs_names[self.selected_tab_index]

    @components(klass=Button)
    def tabs(self):
        """
        Return tab headers as a collection of `Button` widgets.

        Tab text is resolved using `TabsBySpec.tab_label` when configured.
        """
        return ButtonBySpec(
            root=self.component_spec.tabs, label=self.component_spec.tab_label
        )

    def activate(self, tab_name: Union[str, int, re.Pattern]):
        """
        Activate a tab by index, exact text, or regex pattern.

        Parameters:
            tab_name:
                Tab selector expression.

        Raises:
            NoSuchElementException:
                If no matching tab can be resolved.

        Notes:
            - For shared-panel layouts, slot collections are force-refreshed.
            - For per-tab layouts, `selected_tab_index` is updated from the
              resolved tab locator index.
        """
        option = self._find_tab(tab_name)
        if not option:
            raise NoSuchElementException(f"There is no tab: {tab_name}")

        option.click()
        if self.has_shared_panel:
            self.tabs.force_refresh()
        else:
            self.selected_tab_index = int(getattr(option, "_locator").value)

    def _find_tab(self, expression: Union[int, str, re.Pattern]):
        """
        Resolve a tab button by index or EQL-backed semantic selector.

        Parameters:
            expression:
                Index (`int`), exact text (`str`), or regex (`re.Pattern`).
        """
        if isinstance(expression, int):
            return self._find_by_index(expression)
        return self._find_by_eql(expression)

    def _find_by_index(self, index: int):
        """Resolve a tab button by zero-based index."""
        return self.tabs[index]

    def _find_by_eql(self, expression: Union[str, re.Pattern]):
        """Resolve a tab button using an EQL selector built from text/pattern."""
        eql = make_eql_selector(expression)
        return self.tabs[eql]

    @slots
    def panels(self):
        """
        Return tab panels collection materialized via slot rules.

        Returned items may be Elements or Widgets depending on active slot policy.
        """
        return self.component_spec.panels

    @property
    def panel(self):
        """
        Return the currently active panel.

        - Shared-panel mode returns `panels[0]`.
        - Per-tab mode returns `panels[selected_tab_index]`.
        """
        if self.use_shared_panel:
            return self.panels[0]
        return self.panels[self.selected_tab_index]

    @property
    def use_shared_panel(self) -> bool:
        """Return the raw shared-panel flag from component spec."""
        return self.component_spec.use_shared_panel

    def force_refresh(self):
        """
        Clear internal caches and refresh tabs/panels collections.

        This resets:
        - cached tab names
        - tracked selected tab index
        """
        self._tabs_names = []
        self.selected_tab_index = 0
        self.tabs.force_refresh()
        self.panels.force_refresh()

    def verify_has_tab(self, tab: Union[str, re.Pattern]):
        """
        Verify that an item matching the given text/pattern exists.
        """
        tab_button = self._find_tab(tab)
        verify = prepare_expect_object(
            self,
            tab_button,
            False,
            f'Verifying tab "{tab}" presents',
            self._logger,
        )
        return verify.is_not_none()

    def verify_itab_missing(self, tab: Union[str, re.Pattern]):
        """
        Verify that an item matching the given text/pattern does not exist.
        """
        tab_button = self._find_tab(tab)
        verify = prepare_expect_object(
            self,
            tab_button,
            False,
            f'Verifying tab "{tab}" absents',
            self._logger,
        )
        return verify.is_none()

    def assert_has_tab(self, tab: Union[str, re.Pattern]):
        """
        Assert that an item matching the given text/pattern exists.
        """
        tab_button = self._find_tab(tab)
        verify = prepare_expect_object(
            self,
            tab_button,
            True,
            f'Asserting tab "{tab}" presents',
            self._logger,
        )
        return verify.is_not_none()

    def assert_tab_missing(self, tab: Union[str, re.Pattern]):
        """
        Assert that an item matching the given text/pattern does not exist.
        """
        tab_button = self._find_tab(tab)
        verify = prepare_expect_object(
            self,
            tab_button,
            True,
            f'Assertion tab "{tab}" absents',
            self._logger,
        )
        return verify.is_none()
