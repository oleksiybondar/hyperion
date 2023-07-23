from typing import Any

from hyperiontf import (
    WebPage,
    MobileScreen,
    DesktopWindow,
    WebView,
    webview,
    element,
    widget,
    By,
)
from .keypad import Keypad


class Calculator:
    """
    Base Calculator class defining the common interface and functionalities for calculator applications.
    """

    @element
    def result(self) -> Any:
        """
        Locator for the result display element across different platforms.
        """
        return {
            "web": By.id("screen"),
            "mobile": {
                "Android": By.id("com.google.android.calculator:id/result_final")
            },
            "desktop": {"Darwin": By.predicate('label == "main display"')},
        }

    @widget(klass=Keypad)
    def keypad(self) -> Any:
        """
        Widget for the keypad element. It uses the Keypad class for the locator definition.
        """
        # it has a default_locator, so do nothing
        pass

    def evaluate_expression(self, operand, operator, other_operand):
        """
        Evaluates a mathematical expression by entering the operands and operator via the keypad.
        """
        self.keypad.evaluate_expression(operand, operator, other_operand)

    def get_result(self):
        """
        Retrieves the result of the evaluated expression from the result display element.
        """
        result = self.result.get_text()
        if len(result) != 0:
            return float(result)
        return float(self.result.get_attribute("value"))


class WebCalculator(WebPage, Calculator):
    """
    Web-based Calculator class extending the common Calculator functionality.
    """

    pass


class MobileCalculator(MobileScreen, Calculator):
    """
    Mobile-based Calculator class extending the common Calculator functionality.
    """

    pass


class DesktopCalculator(DesktopWindow, Calculator):
    """
    Desktop-based Calculator class extending the common Calculator functionality.
    """

    pass


class WebViewCalculator(WebView, Calculator):
    """
    WebView-based Calculator class extending the common Calculator functionality.
    """

    pass


class HybridCalculator(MobileScreen):
    """
    Hybrid Calculator class defining the interface for working with both native and web elements.
    Includes the WebViewCalculator for web interactions.
    """

    @webview(klass=WebViewCalculator)
    def webview(self):
        """
        WebView widget representing the web-based part of the hybrid calculator.
        """
        pass

    @element
    def address_input(self):
        """
        Locator for the address input element used to open URLs.
        """
        return By.predicate('label == "Address"')

    def open_url(self, url: str):
        """
        Opens a URL by entering it in the address input field and pressing Enter.
        """
        self.address_input.clear_and_fill(f"{url}\ue007")

    def evaluate_expression(self, operand, operator, other_operand):
        """
        Evaluates a mathematical expression within the WebView part of the hybrid calculator.
        """
        self.webview.evaluate_expression(operand, operator, other_operand)

    def get_result(self):
        """
        Retrieves the result of the evaluated expression from the WebView part of the hybrid calculator.
        """
        return self.webview.get_result()
