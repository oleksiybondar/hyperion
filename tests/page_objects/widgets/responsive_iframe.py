from typing import Any

from hyperiontf import IFrame, By, element


class ResponsiveIFrame(IFrame):
    @element
    def responsive_element1(self) -> Any:
        return {
            "xs": By.css(".box-xs.el1"),
            "sm": By.css(".box-sm.el1"),
            "md": By.css(".box-md.el1"),
            "lg": By.css(".box-lg.el1"),
            "xl": By.css(".box-xl.el1"),
            "xxl": By.css(".box-xxl.el1"),
        }

    @element
    def responsive_element2(self) -> Any:
        return {
            "xs": By.css(".box-xs.el2"),
            "sm": By.css(".box-sm.el2"),
            "md": By.css(".box-md.el2"),
            "lg": By.css(".box-lg.el2"),
            "xl": By.css(".box-xl.el2"),
            "xxl": By.css(".box-xxl.el2"),
        }

    @element
    def responsive_element3(self) -> Any:
        return {
            "xs": By.css(".box-xs.el3"),
            "sm": By.css(".box-sm.el3"),
            "md": By.css(".box-md.el3"),
            "lg": By.css(".box-lg.el3"),
            "xl": By.css(".box-xl.el3"),
            "xxl": By.css(".box-xxl.el3"),
        }
