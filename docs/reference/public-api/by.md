← [Back to Documentation Index](/docs/index.md)  
← Previous: [Elements](/docs/reference/public-api/elements.md)  
→ Next: [ActionBuilder](/docs/reference/public-api/action-builder.md)

---
# By

`By` represents a **typed locator descriptor** used by Hyperion to identify elements in the UI.

It serves a role similar to Selenium’s `By`, but is intentionally framework-owned and framework-controlled.

In Hyperion:
- locators are **objects**, not strings
- locator intent is explicit
- context handling is declarative, not manual

---

## What `By` is

`By` is a **value object** that describes *how* an element should be located.

It does **not**:
- locate elements eagerly
- perform queries
- hold references to UI elements

Instead, it describes **locator intent**, which Hyperion later resolves:
- in the correct context
- with retries and recovery
- according to hierarchy rules

Every `Element`, `Elements`, `Widget`, `IFrame`, and `WebView` declaration ultimately relies on a `By` instance.

---

## Why Hyperion uses `By` objects instead of strings

Hyperion deliberately avoids raw selector strings.

Using a structured locator object allows the framework to:

- distinguish locator *type* (id, css, xpath, etc.)
- preserve semantic meaning for logs and diagnostics
- attach metadata needed for retries and recovery
- control **context boundaries** during resolution
- keep locator resolution backend-agnostic

A raw string cannot reliably carry this information.

---

## Context awareness and hierarchy scoping

By default, a `By` locator is resolved **relative to the current hierarchy context**.

This means:
- inside a `Widget`, it resolves within the widget root
- inside an `IFrame`, it resolves inside the iframe document
- inside a `WebView`, it resolves inside the active web context

This behavior is automatic and requires no user action.

Context handling is derived from the Page Object hierarchy —  
tests should not manage it manually.

---

## Explicit document-scoped resolution

In advanced UI structures, elements may exist **outside the current hierarchy**.

Examples include:
- dropdown menus rendered in portals
- overlays attached directly to the document body
- detached popups or global menus

To support these cases, `By` provides a way to **explicitly restart resolution from the document root**.

### `from_document()`

`from_document()` marks a locator as **document-scoped**.

When used:
- Hyperion intentionally bypasses the current hierarchy
- resolution starts from the active document root
- the decision is explicit and visible in logs

```python
from hyperiontf import By

By.css(".MuiMenuItem-root").from_document()
```

This is functionally similar to using XPath with `//`,
but makes the scope decision **explicit and declarative**.

---

## When to use `from_document()`

Use document-scoped locators **only when hierarchy scoping is insufficient**, such as:

- options rendered outside a dropdown trigger subtree
- UI frameworks that use portals or overlays
- elements intentionally detached from their logical owner

Do **not** use `from_document()`:
- to bypass poor Page Object design
- as a replacement for proper widget composition
- for convenience when relative locators are sufficient

This API exists to model **real-world UI constraints**, not to encourage manual scoping.

---

## Common locator factories

`By` provides a small, explicit set of factory methods.

Examples:

```python
from hyperiontf import By

By.id("submit")
By.css(".primary-button")
By.xpath("//button[@type='submit']")
By.name("username")
By.text("Continue")
```

The exact set of supported strategies is framework-defined.
Users should rely only on documented factories.

---

## Usage in Page Objects

`By` is used exclusively inside declarative definitions.

Example:

```python
from hyperiontf import WebPage, element, By


class LoginPage(WebPage):

    @element
    def username(self):
        return By.id("username")

    @element
    def password(self):
        return By.id("password")

    @element
    def submit(self):
        return By.css("button[type='submit']")
```

Important characteristics:
- the `By` object is returned, not executed
- resolution happens later, during interaction
- context is derived from hierarchy, not user code

---

## What `By` does *not* do

`By` intentionally does **not**:

- expose driver-level APIs
- perform manual context switching
- accept arbitrary user-defined strategies
- execute queries eagerly
- guarantee uniqueness by itself

Those responsibilities belong to:
- `Element` / `Elements`
- the retry and recovery system
- the locator resolution engine

---

## Design guarantees

When you use `By`, Hyperion guarantees:

- resolution occurs in the correct context
- retries and stale recovery are applied
- resolution attempts are logged
- failures include locator intent, not just raw selectors

This is why locator objects — not strings — are fundamental.

---

## Summary

`By` exists to make locators:

- explicit
- typed
- context-aware
- debuggable
- framework-controlled

It is intentionally simple —  
and intentionally **not extensible by users**.

> Locators describe *what to look for*.  
> Hyperion decides *how and when* to look.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Elements](/docs/reference/public-api/elements.md)  
→ Next: [ActionBuilder](/docs/reference/public-api/action-builder.md)
