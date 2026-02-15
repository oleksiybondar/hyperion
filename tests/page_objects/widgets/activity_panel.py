from __future__ import annotations

from typing import Any

from hyperiontf import By, Widget, element, elements


class ActivityPanel(Widget):
    @element
    def title(self) -> Any:
        return By.css("strong")

    @elements
    def activity_items(self) -> Any:
        return By.css("li")
