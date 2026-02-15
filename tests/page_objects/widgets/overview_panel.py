from __future__ import annotations

from typing import Any

from hyperiontf import By, Widget, element


class OverviewPanel(Widget):
    @element
    def title(self) -> Any:
        return By.css("strong")

    @element
    def unique_summary(self) -> Any:
        return By.xpath(".//p[contains(., 'simple content block')]")
