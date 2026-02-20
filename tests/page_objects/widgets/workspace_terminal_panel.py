from __future__ import annotations

from typing import Any

from hyperiontf import By, Widget, element


class WorkspaceTerminalPanel(Widget):
    @element
    def title(self) -> Any:
        return By.css(".panel-title")

    @element
    def unique_terminal_session_output(self) -> Any:
        return By.id("unique-terminal-session-output")
