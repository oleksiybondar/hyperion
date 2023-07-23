from typing import Any

from hyperiontf import WebPage, By, element, iframe
from .widgets.responsive_iframe import ResponsiveIFrame


class IframeWithResponsive(WebPage):
    @element
    def xs_button(self) -> Any:
        return By.css(".button-container .button:nth-of-type(1)")

    @element
    def sm_button(self) -> Any:
        return By.css(".button-container .button:nth-of-type(2)")

    @element
    def md_button(self) -> Any:
        return By.css(".button-container .button:nth-of-type(3)")

    @element
    def lg_button(self) -> Any:
        return By.css(".button-container .button:nth-of-type(4)")

    @element
    def xl_button(self) -> Any:
        return By.css(".button-container .button:nth-of-type(5)")

    @element
    def xxl_button(self) -> Any:
        return By.css(".button-container .button:nth-of-type(6)")

    @iframe(klass=ResponsiveIFrame)
    def iframe(self) -> Any:
        return By.css("iframe")
