from typing import Any

from hyperiontf import Widget, widget, By
from .single_widget import SingleWidget


class NestedWidget(Widget):
    @widget(klass=SingleWidget)
    def child_widget(self) -> Any:
        return By.css(".widget")
