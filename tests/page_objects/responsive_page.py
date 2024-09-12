from typing import Any

from hyperiontf import WebPage, By, element


class ResponsivePage(WebPage):
    @element
    def responsive_element1(self) -> Any:
        return {
            "xs": By.css(".box-xs.el1"),
            # making an alternative in locator for SM port, because by some reason it fails with Chromium
            # this is for CI Only, not reproducible locally
            "sm": By.css(".box-sm.el1, .box-md.el1"),
            "md": By.css(".box-md.el1"),
            "lg": By.css(".box-lg.el1"),
            "xl": By.css(".box-xl.el1"),
            "xxl": By.css(".box-xxl.el1"),
        }

    @element
    def responsive_element2(self) -> Any:
        return {
            "xs": By.css(".box-xs.el2"),
            # making an alternative in locator for SM port, because by some reason it fails with Chromium
            # this is for CI Only, not reproducible locally
            "sm": By.css(".box-sm.el2, .box-md.el2"),
            "md": By.css(".box-md.el2"),
            "lg": By.css(".box-lg.el2"),
            "xl": By.css(".box-xl.el2"),
            "xxl": By.css(".box-xxl.el2"),
        }

    @element
    def responsive_element3(self) -> Any:
        return {
            "xs": By.css(".box-xs.el3"),
            # making an alternative in locator for SM port, because by some reason it fails with Chromium
            # this is for CI Only, not reproducible locally
            # TODO: fix it in newer releases
            "sm": By.css(".box-sm.el3, .box-md.el3"),
            "md": By.css(".box-md.el3"),
            "lg": By.css(".box-lg.el3"),
            "xl": By.css(".box-xl.el3"),
            "xxl": By.css(".box-xxl.el3"),
        }
