← [Back to Documentation Index](/docs/index.md)  
← Previous: [Logging Behavior](/docs/reference/behavior-contracts/logging.md)  
→ Next: [Reusable Widget Patterns](/docs/examples/patterns/reusable-widgets.md)

---

# 7.1 Cross-Platform Calculator Example

This example demonstrates a core Hyperion principle:

> **The same test flow and Page Object Model can be reused across platforms and technology stacks without branching test logic.**

The calculator scenario is intentionally simple, but it is not a toy.  
It represents a real-world situation where:

- the same user workflow exists on multiple platforms
- each platform is implemented using different UI technologies
- test intent and assertions remain identical

This document explains **how the pieces fit together**, while relying on documented framework guarantees for the underlying mechanics.

---

## What this example demonstrates

This example shows how Hyperion enables:

- a **shared, platform-agnostic test flow**
- a **single Page Object contract**
- **platform- and OS-specific locator declarations**
- runtime resolution from **locator → element → interaction**

The important point for readers is: Page Objects declare locator choices in a structured way, and Hyperion resolves the correct one at runtime based on the active execution context.

If you want the formal rules behind this, refer to:

- `/docs/reference/behavior-contracts/locator-resolution.md`
- `/docs/reference/behavior-contracts/context-switching.md`

---

## Project layout used in this example

The calculator demo can be thought of as three layers:

1. **Tests** – platform entry points
2. **Page Objects** – shared contract + platform types
3. **Widgets** – reusable components used by Page Objects

A simplified layout:

```python
tests/
  test_calculator_web.py
  test_calculator_mobile.py
  test_calculator_desktop.py
  test_calculator_hybrid.py

page_objects/
  calculator.py
  keypad.py
```

In production suites, these tests often live in separate platform-specific folders.  
This example keeps them conceptually together to emphasize reuse.

---

## Shared test flow (platform-agnostic logic)

The core business workflow is written once and reused everywhere.

```python
from hyperiontf import expect

def calculator_flow(page) -> None:
    page.evaluate_expression(5.6, "+", 10.4)
    result = page.get_result()
    expect(result).to_be(16)
```

Key observations:

- the flow accepts a single argument: a **Page Object instance**
- no platform or OS branching exists in the flow
- the flow ends with an **explicit assertion**

This is the key pattern: tests express intent once, platforms provide compatible Page Objects.

---

## Platform entry points: same flow, different execution contexts

Platform tests differ only in how the Page Object is started and navigated.  
The flow stays the same.

```python
import pytest

@pytest.mark.tags("Web", "Calculator", "Cross-platform")
def test_web_calculator():
    page = WebCalculator.start_browser()
    page.open("https://example.test/calculator")
    calculator_flow(page)


@pytest.mark.tags("Mobile", "Calculator", "Android", "Cross-platform")
def test_android_calculator():
    caps = {
        # NOTE: capability values are illustrative; use your own desired setup.
        "automation": "appium",
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "appPackage": "<your.calculator.package>",
        "appActivity": "<your.calculator.activity>",
    }
    page = MobileCalculator.launch_app(caps)
    calculator_flow(page)


@pytest.mark.tags("Desktop", "Calculator", "Cross-platform")
def test_desktop_calculator():
    caps = {
        # NOTE: capability values are illustrative; use your own desired setup.
        "automation": "appium",
        "platformName": "Mac",
        "automationName": "Mac2",
        "bundleId": "<your.desktop.bundle.id>",
    }
    page = DesktopCalculator.launch_app(caps)
    calculator_flow(page)


@pytest.mark.tags("Mobile", "Web", "HybridApp", "iOS", "Cross-platform")
def test_hybrid_calculator():
    caps = {
        # NOTE: capability values are illustrative; use your own desired setup.
        "automation": "appium",
        "platformName": "iOS",
        "automationName": "XCUITest",
        "bundleId": "com.apple.mobilesafari",
        "includeSafariInWebviews": True,
    }
    page = HybridCalculator.launch_app(caps)
    page.open_url("https://example.test/calculator")
    calculator_flow(page)
```

This demonstrates the cross-platform promise:

- different execution contexts
- same Page Object interface
- same shared flow
- same assertion

---

## Base Calculator contract: one interface, many implementations

The shared contract is expressed as a base class that defines:

- a `result` element
- a `keypad` widget
- shared behavior (`evaluate_expression`)
- shared result accessor (`get_result`)

The values below are placeholders, but the **structure** is real and matches Hyperion usage.

```python
from typing import Any
from selenium.webdriver.common.by import By

from hyperiontf.pages import WebPage, MobileScreen, DesktopWindow, WebView
from hyperiontf.pages.decorators import element, elements, widget, webview
from hyperiontf.widgets import Widget

class Keypad(Widget):
    @property
    def default_locator(self):
        return {
            "web": By.css_selector("<web keypad root>"),
            "mobile": {"Android": By.id("<android keypad root>")},
            "desktop": {"Darwin": By.xpath("<mac keypad root>")},
        }

    @elements
    def buttons(self):
        return {
            "web": By.tag_name("button"),
            "mobile": {"Android": By.class_name("<android button class>")},
            "desktop": {"Darwin": By.xpath("<mac button xpath>")},
        }

    def evaluate_expression(self, operand: float, operator: str, other_operand: float) -> None:
        # Example only: real implementation maps operand/operator to button indexes/labels.
        # The important part is: behavior is shared; locators are platform/OS-specific.
        ...

class Calculator:
    @element
    def result(self) -> Any:
        return {
            "web": By.id("<web result id>"),
            "mobile": {"Android": By.id("<android result id>")},
            "desktop": {"Darwin": By.predicate('<mac predicate for display>')},
        }

    @widget(klass=Keypad)
    def keypad(self) -> Any:
        # The widget has default_locator, so no explicit locator needed here.
        pass

    def evaluate_expression(self, operand: float, operator: str, other_operand: float) -> None:
        self.keypad.evaluate_expression(operand, operator, other_operand)

    def get_result(self) -> float:
        # Example only: in practice you may read text or an attribute depending on platform.
        value = self.result.get_text()
        return float(value)
```

### Runtime resolution: locator vs element (why this is not “magic”)

- Page Objects declare *locator choices* (often as platform/OS keyed mappings).
- When a test runs, Hyperion already knows the active platform context.
- Hyperion resolves the correct locator into a real element **at runtime**.
- Tests never pick locators manually — they use Page Object behavior.

This keeps tests clean while still being explicit and deterministic.

---

## Platform classes: minimal per-platform code

Platform-specific classes are typically thin because the shared contract already defines behavior.

```python
class WebCalculator(WebPage, Calculator):
    pass

class MobileCalculator(MobileScreen, Calculator):
    pass

class DesktopCalculator(DesktopWindow, Calculator):
    pass

class WebViewCalculator(WebView, Calculator):
    pass
```

This is the reuse multiplier:

- behavior and contract live once
- platform base class selects the environment
- locator mapping selects the runtime branch

---

## Hybrid application case (WebView + native)

For hybrid apps, the Page Object can declare a WebView boundary and forward behavior into it.

```python
class HybridCalculator(MobileScreen):
    @webview(klass=WebViewCalculator)
    def webview(self):
        pass

    @element
    def address_input(self):
        return By.predicate('<ios safari address field predicate>')

    def open_url(self, url: str) -> None:
        self.address_input.clear_and_fill(f"{url}\ue007")

    def evaluate_expression(self, operand: float, operator: str, other_operand: float) -> None:
        self.webview.evaluate_expression(operand, operator, other_operand)

    def get_result(self) -> float:
        return self.webview.get_result()
```

The important thing: the shared test flow stays the same — only the Page Object wiring differs.

---

## Why this pattern works in real test suites

This structure scales because:

- intent is written once (shared flow)
- platform differences stay behind Page Objects
- new platforms add implementations, not test rewrites

The key boundary is:

- tests talk to **behavior**
- Page Objects declare **locator choices**
- runtime resolves choices into **elements**
- element actions occur in the correct **context**

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Logging Behavior](/docs/reference/behavior-contracts/logging.md)  
→ Next: [Reusable Widget Patterns](/docs/examples/patterns/reusable-widgets.md)
