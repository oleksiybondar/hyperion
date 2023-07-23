from typing import Any

from hyperiontf import Widget, element, By


class ControlPanel(Widget):
    @element
    def re_render_single_element_button(self) -> Any:
        return By.css(".control-button:nth-child(1)")

    @element
    def re_render_multiple_elements_button(self) -> Any:
        return By.css(".control-button:nth-child(2)")

    @element
    def re_render_single_widget_button(self) -> Any:
        return By.css(".control-button:nth-child(3)")

    @element
    def re_render_widget_child_button(self) -> Any:
        return By.css(".control-button:nth-child(4)")

    @element
    def re_render_nested_widgets_button(self) -> Any:
        return By.css(".control-button:nth-child(5)")

    def re_render_single_element(self):
        self.re_render_single_element_button.click()

    def re_render_multiple_elements(self):
        self.re_render_multiple_elements_button.click()

    def re_render_single_widget(self):
        self.re_render_single_widget_button.click()

    def re_render_widget_child(self):
        self.re_render_widget_child_button.click()

    def re_render_nested_widgets(self):
        self.re_render_nested_widgets_button.click()
