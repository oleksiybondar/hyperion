← [Back to Documentation Index](/docs/index.md)  
← Previous: [Responsive (Viewport-Specific) Locators](/docs/how-to/responsive-locators.md)  
→ Next: [Platform-Agnostic Locators](/docs/how-to/platform-agnostic-locators.md)

---

# 4.5 OS-Specific Locators

OS-specific locators let you keep one logical Page Object when the same feature exists across environments but requires different selectors per operating system.

This is common when:

- automation stacks expose different accessibility trees
- native UI frameworks name elements differently per OS
- desktop platforms differ (Windows vs macOS vs Linux)
- mobile platforms differ (Android vs iOS)

OS-specific locators are an explicit modeling tool: you declare all OS branches you support, and Hyperion resolves the correct one at runtime.

For background on resolution dimensions, see:  
`/docs/core-concepts/locator-resolution.md`

---

## Supported OS keys

Hyperion’s OS keys follow a fixed set of identifiers.

```python
from typing import Literal

OSType = Literal[
    "Windows",
    "Darwin",  # platform.system() returns 'Darwin' for macOS
    "Linux",
    "Android",
    "iOS",
]
```

When you declare OS-specific locators, keys must match these OS identifiers.

---

## OS-specific locators must be explicit

There is no `default` fallback for OS-specific variation.

- every OS branch you want to support must be explicitly declared
- if you omit an OS branch, that locator is not defined for that OS

This prevents accidental cross-OS behavior and keeps the model deterministic.

---

## Declaring OS-specific `@element`

OS variation is typically nested under a platform key (mobile or desktop), and then split by OS.

```python
from selenium.webdriver.common.by import By
from hyperiontf.pages.decorators import element

class SettingsScreen:
    @element
    def save_button(self):
        return {
            "mobile": {
                "Android": By.id("<android save id>"),
                "iOS": By.predicate("<ios predicate for save>"),
            },
            "desktop": {
                "Windows": By.name("<windows name>"),
                "Darwin": By.predicate("<mac predicate>"),
                "Linux": By.css_selector("<linux selector if applicable>"),
            },
        }
```

Notes:

- the structure is a declaration of supported environments
- tests never reference OS keys
- Hyperion selects the correct branch at runtime

---

## OS-specific `@elements` collections

Collections can vary by OS as well.

```python
from selenium.webdriver.common.by import By
from hyperiontf.pages.decorators import elements

class FilePicker:
    @elements
    def items(self):
        return {
            "desktop": {
                "Windows": By.xpath("<windows item xpath>"),
                "Darwin": By.xpath("<mac item xpath>"),
            }
        }
```

The consumer code remains stable: `items` always returns resolved elements, regardless of OS.

---

## Where OS-specific variation should live

Prefer encoding OS variability:

1. inside the widget that owns the component, or
2. in the contract-level Page Object

Avoid OS branching in tests.

This is consistent with the example patterns from Section 7:

- tests interact with behavior
- Page Objects declare environment variation
- runtime resolves locators into real elements

---

## Common mistakes

### Using `default` for OS variation
`default` is viewport-only.

### Mixing OS and viewport keys at the same level
OS and viewport are different dimensions. If you combine them, keep the structure clear and intentional.

### Encoding “business differences” as OS differences
OS-specific locators are for selector differences, not for fundamentally different behavior or requirements. If behavior truly differs, model it as behavior differences in Page Objects or widgets.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Responsive (Viewport-Specific) Locators](/docs/how-to/responsive-locators.md)  
→ Next: [Platform-Agnostic Locators](/docs/how-to/platform-agnostic-locators.md)
