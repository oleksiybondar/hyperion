from __future__ import annotations

from typing import Any

from hyperiontf import By, Widget, element


class WorkspaceGitPanel(Widget):
    @element
    def title(self) -> Any:
        return By.css(".panel-title")

    @element
    def unique_git_commit_stage(self) -> Any:
        return By.id("unique-git-commit-stage")
