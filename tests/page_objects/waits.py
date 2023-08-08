from typing import Any

from hyperiontf import WebPage, By, element, elements, widget

from page_objects.widgets.wiats_control_panel import WaitsControlPanel


class WaitsPage(WebPage):
    @widget(klass=WaitsControlPanel)
    def control_panel(self) -> Any:
        return By.id("control-panel")

    @element
    def disabled_button(self) -> Any:
        return By.id("static-button")

    @element
    def invisible_element(self) -> Any:
        return By.id("disappearing-element")

    @element
    def present_element(self) -> Any:
        return By.id("always-visible")

    @element
    def new_element(self) -> Any:
        return By.id("new-element")

    @element
    def animated_element(self) -> Any:
        return By.id("dynamic-element")

    @elements
    def elements_array(self) -> Any:
        return By.css(".array-elements .array-element")
