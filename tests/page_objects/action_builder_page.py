from typing import Any, List

from hyperiontf import WebPage, By, element, elements


class ActionBuilderPage(WebPage):

    @element
    def canvas(self) -> Any:
        return By.id("myCanvas")

    @element
    def popup_menu(self) -> Any:
        return By.id("popupMenu")

    @element
    def text_area1(self) -> Any:
        return By.id("textArea1")

    @element
    def text_area2(self) -> Any:
        return By.id("textArea2")

    @elements
    def rows(self) -> List[Any]:
        return By.css(".draggable")
