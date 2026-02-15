from __future__ import annotations

from typing import Any

from hyperiontf import By, Widget, element


class UsersPanel(Widget):
    @element
    def title(self) -> Any:
        return By.css("strong")

    @element
    def users_table(self) -> Any:
        return By.id("tabs-1to1-users-table")
