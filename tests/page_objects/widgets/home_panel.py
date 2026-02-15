from __future__ import annotations

from typing import Any

from hyperiontf import By, Widget, element


class HomePanel(Widget):
    @element
    def title(self) -> Any:
        return By.css("strong")

    @element
    def unique_welcome(self) -> Any:
        return By.xpath(
            ".//p[contains(., 'Welcome. This content is replaced on each tab selection.')]"
        )
