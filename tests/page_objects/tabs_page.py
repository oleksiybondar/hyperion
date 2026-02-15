from __future__ import annotations

from hyperiontf import By, SlotPolicyRule, TabsBySpec, WebPage
from hyperiontf.ui.components.decorators.page_object_helpers import tabs

from .widgets.activity_panel import ActivityPanel
from .widgets.help_panel import HelpPanel
from .widgets.home_panel import HomePanel
from .widgets.overview_panel import OverviewPanel
from .widgets.profile_panel import ProfilePanel
from .widgets.settings_panel import SettingsPanel
from .widgets.users_panel import UsersPanel


class TabsPage(WebPage):
    """
    Page Object for `tabs.html`.

    Covers:
    - Variant A: 1:1 tab-to-panel mapping with visibility toggling
    - Variant B: shared single panel with content re-render on tab click
    """

    @tabs
    def tabs_1to1(self) -> TabsBySpec:
        return TabsBySpec(
            root=By.id("tabs-1to1"),
            tabs=By.css("#tabs-1to1-buttons .tab-button"),
            panels=By.css("#tabs-1to1-contents .tab-content"),
            tab_label=By.css(".tab-label"),
            slot_policies=[
                SlotPolicyRule(0, OverviewPanel),
                SlotPolicyRule(1, UsersPanel),
                SlotPolicyRule(2, SettingsPanel),
            ],
        )

    @tabs
    def tabs_rerender(self) -> TabsBySpec:
        return TabsBySpec(
            root=By.id("tabs-rerender"),
            tabs=By.css("#tabs-rerender-buttons .tab-button"),
            panels=By.css("#tabs-rerender-panel"),
            use_shared_panel=True,
            tab_label=By.css(".tab-label"),
            slot_policies=[
                SlotPolicyRule(0, HomePanel),
                SlotPolicyRule(1, ProfilePanel),
                SlotPolicyRule("Activity", ActivityPanel),
                SlotPolicyRule("Help", HelpPanel),
            ],
        )
