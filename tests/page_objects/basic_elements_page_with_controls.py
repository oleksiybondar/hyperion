from typing import Any

from hyperiontf import widget, By
from .widgets.re_render_control_panel import ControlPanel
from .basic_elements_page import BasicElementsSearch


class BasicElementsSearchWithControls(BasicElementsSearch):
    @widget(klass=ControlPanel)
    def re_render_panel(self) -> Any:
        return By.css(".control-panel")
