from typing import Any

from hyperiontf import IFrame, By, element, iframe
from .basic_elements_iframe import BasicElementsIframe


class ChildIframe(IFrame):
    # page title
    @element
    def page_header(self) -> Any:
        return By.css("h1.child-title")

    @element
    def re_render_iframe_button(self) -> Any:
        return By.css(".control-button-child")

    @iframe(klass=BasicElementsIframe)
    def dynamic_iframe(self) -> Any:
        return By.id("test-iframe-child")
