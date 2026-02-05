← [Back to Documentation Index](/docs/index.md)  
← Previous: [OS-Specific Locators](/docs/how-to/os-specific-locators.md)  
→ Next: [Nested Widgets](/docs/how-to/nested-widgets.md)

---

# 4.6 Platform-Agnostic Locators

Platform-agnostic locators are for cases where the same logical element can be located in a consistent way across platforms.

This is the “happy path”:

- a locator is static and universally applicable
- no platform/OS/viewport mapping is needed
- resolution logic is not involved

Platform-agnostic locators keep Page Objects simple and are the preferred choice when they work reliably.

For background on the resolution model, see:  
`/docs/core-concepts/locator-resolution.md`

---

## Supported platform keys

Platforms in Hyperion use a fixed set of identifiers.

{codeblock}python
from typing import Literal

PlatformType = Literal[
    "web",
    "mobile",
    "desktop",
]
{codeblock}

Platform-agnostic locators often do not need to mention these keys at all.

---

## The simplest case: static locators

If a locator does not declare variation, it is treated as static.

{codeblock}python
from selenium.webdriver.common.by import By
from hyperiontf.pages.decorators import element

class LoginPage:
    @element
    def username(self):
        return By.id("<shared username id>")
{codeblock}

This is platform-agnostic if it applies everywhere the Page Object is used.

---

## When “platform-agnostic” means “consistent contract”

Often, a Page Object defines a consistent interface across platforms even when locators differ.

That is not a platform-agnostic locator; it is a platform-agnostic **contract**.

This is the pattern shown in the calculator example:

- the test flow is platform-agnostic
- the Page Object API is platform-agnostic
- locators may still vary by platform/OS

Choose the simplest locator type that works:

1. static locator (no mapping)
2. responsive locator (viewport mapping)
3. platform/OS mapping (explicit environment branches)

---

## Pattern: keep locators agnostic inside widgets

Widgets are often the best place for agnostic locators because they map to UI components that repeat.

If a widget can use stable selectors across platforms, it becomes broadly reusable.

{codeblock}python
from selenium.webdriver.common.by import By
from hyperiontf.pages.decorators import elements
from hyperiontf.widgets import Widget

class Tabs(Widget):
    @elements
    def items(self):
        return By.css_selector("<stable selector for tabs>")
{codeblock}

If later one platform diverges, you can introduce platform/OS mapping inside the widget without changing the public widget API.

---

## Common mistakes

### Declaring mappings prematurely
If a static locator works reliably, use it. Mappings are for real divergence.

### Confusing “agnostic locator” with “agnostic tests”
Tests can be platform-agnostic even when locators vary. That’s a contract-level reuse strategy, not a locator-level one.

### Using platform mappings as a convenience
Platform mappings are powerful, but they should represent genuine structural differences, not preferences.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [OS-Specific Locators](/docs/how-to/os-specific-locators.md)  
→ Next: [Nested Widgets](/docs/how-to/nested-widgets.md)
