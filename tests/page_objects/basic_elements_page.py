from typing import Any

from hyperiontf import WebPage, By, element, elements, widget, widgets
from .widgets.nested_widget import NestedWidget
from .widgets.nested_widgets import NestedWidgets
from .widgets.single_widget import SingleWidget


class BasicElementsSearch(WebPage):
    # Single Elements
    @element
    def single_element_1(self) -> Any:
        return By.id("single-element-1")

    @element
    def single_element_2(self) -> Any:
        return By.test_id("single-element-2")

    @element
    def single_element_3(self) -> Any:
        return By.css("[data-testid='single-element-3']")

    # Multiple Elements
    @elements
    def multiple_elements(self) -> Any:
        return By.css(".multiple-element")

    # Single Widget
    @widget(klass=SingleWidget)
    def single_widget(self) -> Any:
        return By.css("[data-testid='single-widget-1']")

    # Nested Single Widget
    @widget(klass=NestedWidget)
    def nested_single_widget(self) -> Any:
        return By.xpath("//*[@data-testid='nested-single-widget']")

    # Multiple Widgets
    @widgets(klass=SingleWidget)
    def multiple_simple_widgets(self) -> Any:
        return By.css("[data-testid^='multiple-widget-']")

    # Widget with nested widgets
    @widget(klass=NestedWidgets)
    def widget(self) -> Any:
        return By.test_id("nested-multiple-widget")

    # Clickable Element for Action Verification
    @element
    def clickable_element(self) -> Any:
        return By.css("[data-testid='clickable-element']")

    # Input Element for Action Verification
    @element
    def input_element(self) -> Any:
        return By.css("[data-testid='input-element']")
