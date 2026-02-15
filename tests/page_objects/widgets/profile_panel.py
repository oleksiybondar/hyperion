from __future__ import annotations

from typing import Any

from hyperiontf import By, Widget, element


class ProfilePanel(Widget):
    @element
    def title(self) -> Any:
        return By.css("strong")

    @element
    def profile_name(self) -> Any:
        return By.id("profile-name")
