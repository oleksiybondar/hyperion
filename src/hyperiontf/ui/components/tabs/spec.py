from typing import Optional

from hyperiontf.typing import LocatorTree
from hyperiontf.ui.components.spec import ComponentSpec
from hyperiontf.ui.components.typing import SlotPolicyType


class TabsBySpec(ComponentSpec):
    """
    Specification object for a Tabs component.

    TabsBySpec defines the structural locators and slot resolution rules
    required to model tab navigation and tab-associated content in a
    declarative, backend-agnostic way.

    A Tabs component consists of:
    - a logical root that scopes tab resolution
    - a collection of tab triggers (`tabs`)
    - a collection of content panels (`panels`)
    - an optional locator for tab labels (`tab_label`)
    - an optional slot policy for panel materialization

    Parameters:
        root:
            Locator tree describing the logical root of the tabs component.

        tabs:
            Locator tree describing the collection of tab triggers.

        panels:
            Locator tree describing tab content panels.

            This field is intentionally plural because multi-panel tabs are
            the default model.

        use_shared_panel:
            Whether tabs use a single shared panel container whose content is
            replaced on tab switch.

            When True, the runtime resolves active content via `panels[0]`
            after switching tabs.

        tab_label:
            Optional locator tree describing a label element relative to each
            tab trigger, used for identity/text resolution when needed.

        slot_policies:
            Optional ordered list of slot policy rules controlling how panel
            content is materialized.

    Notes:
        - TabsBySpec is declarative only; it performs no interaction,
          switching, waiting, or visibility checks by itself.
        - Panel lookup strategy (multi-panel vs shared panel) is controlled
          by `use_shared_panel`.
    """

    def __init__(
        self,
        root: LocatorTree,
        tabs: LocatorTree,
        panels: LocatorTree,
        use_shared_panel: bool = False,
        tab_label: Optional[LocatorTree] = None,
        slot_policies: Optional[SlotPolicyType] = None,
        close_tab_button: Optional[LocatorTree] = None,
    ):
        super().__init__(root, slot_policies)
        self.tabs = tabs
        self.panels = panels
        self.use_shared_panel = use_shared_panel
        self.tab_label = tab_label
        self.close_tab_button = close_tab_button
