from typing import Any

from hyperiontf import WebPage, By, element, iframe
from .widgets.basic_elements_iframe import BasicElementsIframe
from .widgets.child_iframe import ChildIframe


class IframesPage(WebPage):
    # page title
    @element
    def page_header(self) -> Any:
        return By.css("h1.root-page")

    @element
    def re_render_iframe_button(self) -> Any:
        return By.css(".control-button")

    @iframe(klass=ChildIframe)
    def dynamic_iframe(self) -> Any:
        return By.id("test-iframe")

    @iframe(klass=BasicElementsIframe)
    def static_iframe(self) -> Any:
        return By.id("static-test-iframe")
