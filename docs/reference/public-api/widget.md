# 5.4 Widget

← [/docs/reference/public-api/desktopwindow.md](/docs/reference/public-api/desktopwindow.md)  
→ [/docs/reference/public-api/iframe.md](/docs/reference/public-api/iframe.md)

---

`Widget` represents a **nested Page Object** inside another Page Object.

It is used to model **structured, repeatable, or logically grouped UI fragments** such as:
- forms
- panels
- cards
- table rows
- dialogs
- composite controls

A widget behaves like an element **and** like a container at the same time.

---

## Conceptual role of Widget

A `Widget` exists to solve a modeling problem, not an interaction problem.

Think of it as:

> “An element that owns other elements.”

Key properties:
- a widget has a **root locator**
- inside that root, it can define:
  - elements
  - collections of elements
  - other widgets
  - iframes
  - webviews
- widgets participate in the **same automatic context resolution** as pages

Widgets do **not** introduce new interaction APIs.  
They reuse the same API surface as `Element`.

---

## How Widgets differ from Elements

| Aspect | Element | Widget |
|-----|------|------|
| Represents | Single UI node | Structured UI fragment |
| Can contain children | ❌ | ✅ |
| Has its own locator | ✅ | ✅ |
| Supports Element API | ✅ | ✅ |
| Defines nested structure | ❌ | ✅ |

In practice:
- **Element** → “leaf”
- **Widget** → “branch”

---

## Defining a Widget

Widgets are defined by subclassing `Widget` and describing structure inside it.

```python
from hyperiontf import Widget, element, By


class LoginForm(Widget):

    @element
    def email_input(self):
        return By.id("email")

    @element
    def password_input(self):
        return By.id("password")

    @element
    def submit_button(self):
        return By.id("submit")

    def submit(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
```

---

## Attaching a Widget to a Page or another Widget

Widgets are attached using decorators, just like elements.

Available decorators:
- `@widget`
- `@widgets` (collection of widgets)
- `@element`
- `@elements`
- `@iframe`
- `@iframes`
- `@webview`

Unlike `@element`, widget decorators accept a **class reference**.

```python
from hyperiontf import WebPage, widget, By


class LoginPage(WebPage):

    @widget(klass=LoginForm)
    def login_form(self):
        return By.id("login-form")

    def login(self, email: str, password: str) -> None:
        self.login_form.submit(email, password)
```

---

## Widgets vs Elements API

A `Widget` **mimics the Element API**.

This means:
- you can call wait methods on a widget
- you can check visibility / existence
- widgets participate in retries and recovery
- widgets can be used in `expect` / `verify`

Example:

```python
expect(page.login_form.is_visible()).to_be(True)
page.login_form.wait_until_fully_interactable()
```

👉 For the full interaction API, see:
→ [/docs/reference/public-api/element.md](/docs/reference/public-api/element.md)

---

## Widgets and hierarchy

Widgets can be nested arbitrarily:

```
DashboardPage
 └── TableWidget
     └── RowWidget
         └── ActionMenuWidget
```

Each level:
- resolves its own context automatically
- scopes locators to its parent
- logs actions with full hierarchy context

This is the **core strength** of Hyperion’s Page Object Model.

---

## Widgets vs Page Objects

| Feature | Page (WebPage / MobileScreen / DesktopWindow) | Widget |
|------|---------------------------------------------|------|
| Root of session | ✅ | ❌ |
| Can start / launch | ✅ | ❌ |
| Represents whole screen/window | ✅ | ❌ |
| Can be nested | ❌ | ✅ |

Widgets are **never started directly**.  
They always live inside another Page Object.

---

## Recommended usage pattern

Use widgets whenever:
- a UI fragment has internal structure
- the same structure appears multiple times
- behavior belongs to a sub-part of the UI

Avoid:
- large “god pages” with dozens of flat elements
- duplicating locator logic across pages

---

## Summary

- `Widget` is a **structural abstraction**
- it does not invent new APIs
- it **reuses Element API**
- it enables clean, hierarchical modeling
- it is the foundation for scalable Page Object design

For interaction methods and waits, see:
→ [/docs/reference/public-api/element.md](/docs/reference/public-api/element.md)

---

← [/docs/reference/public-api/desktopwindow.md](/docs/reference/public-api/desktopwindow.md)  
→ [/docs/reference/public-api/iframe.md](/docs/reference/public-api/iframe.md)