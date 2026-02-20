from __future__ import annotations

from typing import Any

from hyperiontf import By, SlotPolicyRule, TabsBySpec, WebPage, element, tabs

from .widgets.workspace_files_panel import WorkspaceFilesPanel
from .widgets.workspace_git_panel import WorkspaceGitPanel
from .widgets.workspace_search_panel import WorkspaceSearchPanel
from .widgets.workspace_terminal_panel import WorkspaceTerminalPanel


class TabbedWorkspacesPage(WebPage):
    """
    Page Object for `tabbed_workspaces.html`.

    Models a dynamic tab-host workspace where sidebar actions upsert/activate
    tabs and each tab can be closed.
    """

    @tabs
    def workspace_tabs(self) -> TabsBySpec:
        return TabsBySpec(
            root=By.id("workspace"),
            tabs=By.css("#workspace-tabs [data-tab-activate]"),
            panels=By.css("#workspace-area .panel"),
            close_tab_button=By.xpath("./following-sibling::button[@data-tab-close]"),
            slot_policies=[
                SlotPolicyRule("Files", WorkspaceFilesPanel),
                SlotPolicyRule("Search", WorkspaceSearchPanel),
                SlotPolicyRule("Terminal", WorkspaceTerminalPanel),
                SlotPolicyRule("Git", WorkspaceGitPanel),
            ],
        )

    @element
    def open_files_panel_button(self) -> Any:
        return By.css("#sidebar [data-panel-id='panel-files']")

    @element
    def open_search_panel_button(self) -> Any:
        return By.css("#sidebar [data-panel-id='panel-search']")

    @element
    def open_terminal_panel_button(self) -> Any:
        return By.css("#sidebar [data-panel-id='panel-terminal']")

    @element
    def open_git_panel_button(self) -> Any:
        return By.css("#sidebar [data-panel-id='panel-git']")

    @element
    def workspace_last_action(self) -> Any:
        return By.id("workspace-last-action")

    @element
    def workspace_tabs_empty(self) -> Any:
        return By.id("workspace-tabs-empty")
