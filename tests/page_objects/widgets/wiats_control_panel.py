from typing import Any

from hyperiontf import Widget, element, By


class WaitsControlPanel(Widget):
    @element
    def add_element_button(self) -> Any:
        return By.id("add-element-button")

    @element
    def state_button(self) -> Any:
        return By.id("state-toggle-button")

    @element
    def visibility_button(self) -> Any:
        return By.id("visibility-toggle-button")

    @element
    def remove_element_button(self) -> Any:
        return By.id("remove-element-button")

    @element
    def add_array_element_button(self) -> Any:
        return By.id("add-array-element-button")

    @element
    def remove_array_element_button(self) -> Any:
        return By.id("remove-array-element-button")

    @element
    def remove_array_elements_button(self) -> Any:
        return By.id("remove-array-elements-button")

    @element
    def animation_button(self) -> Any:
        return By.id("animation-button")
