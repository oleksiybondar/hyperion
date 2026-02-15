from __future__ import annotations

from typing import Any

from hyperiontf import By, Widget, element


class SettingsPanel(Widget):
    @element
    def title(self) -> Any:
        return By.css("strong")

    @element
    def language_select(self) -> Any:
        return By.id("tabs-1to1-language")
