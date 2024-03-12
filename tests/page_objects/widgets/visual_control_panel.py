from typing import Any

from hyperiontf import Widget, element, By


class VisualControlPanel(Widget):
    @element
    def dice_1(self) -> Any:
        return By.id("dice1")

    @element
    def dice_2(self) -> Any:
        return By.id("dice2")

    @element
    def dice_3(self) -> Any:
        return By.id("dice3")

    @element
    def dice_4(self) -> Any:
        return By.id("dice4")

    @element
    def dice_5(self) -> Any:
        return By.id("dice5")

    @element
    def dice_6(self) -> Any:
        return By.id("dice6")

    @element
    def resize_blue(self) -> Any:
        return By.id("sizeBlue")

    @element
    def split_purple(self) -> Any:
        return By.id("splitPurple")

    @element
    def change_shapes(self) -> Any:
        return By.id("changeShapes")

    @element
    def toggle_interference(self) -> Any:
        return By.id("toggleInterference")
