from typing import Any

from hyperiontf import Widget, widgets, By
from .single_widget import SingleWidget


class NestedWidgets(Widget):
    @widgets(klass=SingleWidget)
    def child_widgets(self) -> Any:
        return By.css(".widget")
