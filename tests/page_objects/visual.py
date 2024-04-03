from typing import Any

from hyperiontf import WebPage, By, element, widget

from page_objects.widgets.visual_control_panel import VisualControlPanel


class VisualPage(WebPage):
    @widget(klass=VisualControlPanel)
    def control_panel(self) -> Any:
        return By.id("control-area")

    @element
    def dice(self) -> Any:
        return By.css(".dice")
