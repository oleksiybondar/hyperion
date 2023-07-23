from typing import Any

from hyperiontf import WebPage, element, By


class MultipleWindowsTestPage(WebPage):
    """
    Page Object representing the 'Test Page - Multiple Windows'.
    """

    @element
    def basic_link(self) -> Any:
        return By.test_id("basic")

    @element
    def stale_link(self) -> Any:
        return By.test_id("stale")

    @element
    def iframes_link(self) -> Any:
        return By.test_id("iframe")
