from typing import Any

from hyperiontf import Widget, element, By


class SingleWidget(Widget):
    @element
    def child_element(self) -> Any:
        return By.css(".child-element")

    @element
    def not_reachable(self) -> Any:
        return By.css(".i-dont-exist")
