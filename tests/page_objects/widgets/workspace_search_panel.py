from __future__ import annotations

from typing import Any

from hyperiontf import By, Widget, element


class WorkspaceSearchPanel(Widget):
    @element
    def title(self) -> Any:
        return By.css(".panel-title")

    @element
    def unique_search_query_input(self) -> Any:
        return By.id("unique-search-query-input")
