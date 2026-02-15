from __future__ import annotations

from typing import Any

from hyperiontf import By, Widget, element


class HelpPanel(Widget):
    @element
    def title(self) -> Any:
        return By.css("strong")

    @element
    def help_link(self) -> Any:
        return By.id("help-link")
