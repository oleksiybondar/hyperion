from __future__ import annotations

from typing import Any

from hyperiontf import By, Widget, element


class WorkspaceFilesPanel(Widget):
    @element
    def title(self) -> Any:
        return By.css(".panel-title")

    @element
    def unique_files_tree_root(self) -> Any:
        return By.id("unique-files-tree-root")
