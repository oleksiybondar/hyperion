← [Back to Documentation Index](/docs/index.md)  
← Previous: [IFrame](/docs/reference/public-api/iframe.md)  
→ Next: [Element](/docs/reference/public-api/element.md)

---

# WebView

`WebView` represents a **root-level embedded web browsing context**.

- It behaves like a page living inside a host environment (for example: a mobile app shell or embedded browser surface).
- It defines a **top-level context boundary**, similar in spirit to an `IFrame`, but without being nested in page DOM structure.
- It reuses the full `Element` and `Elements` APIs for interaction, waits, assertions, verifications, EQL, and visual checks.
- Context switching is **fully automatic**.

> You never attach to, activate, or switch into a webview manually.  
> Hyperion guarantees that interactions always occur in the correct webview context.

---

## Conceptual role

| Aspect | Meaning |
|---|---|
| Structural container | Yes |
| Hierarchical | Yes |
| Leaf | No |
| Root browsing context | Yes |
| Interaction API | Reuses `Element` |
| Context boundary | Yes |

A `WebView` acts as a **page-like root** inside a larger host (for example, a mobile screen or desktop window).

---

## Relationship to other objects

### WebView vs IFrame

| Aspect | IFrame | WebView |
|---|---|---|
| Position | Part of a web page | Embedded browser surface |
| Parent | Page / Widget | Host screen or window |
| Context type | Nested browsing context | Root browsing context |
| Children | Elements, Widgets, IFrames | Elements, Widgets, IFrames |
| Context switching | Automatic | Automatic |

From the test author’s perspective, both behave the same:
- declare structure
- interact with children
- never manage context manually

---

## Declaring a WebView

A `WebView` is typically declared on a host object (for example: `MobileScreen` or `DesktopWindow`).

```python
from hyperiontf import MobileScreen, WebView, webview


class MainWebView(WebView):
    pass


class HomeScreen(MobileScreen):

    @webview(klass=MainWebView)
    def main_webview(self):
        pass
```

---

## Declaring content inside a WebView

Children are declared on the `WebView` class using the standard element/collection decorators.

```python
from hyperiontf import MobileScreen, WebView, webview, element, elements, By


class MainWebView(WebView):

    @element
    def login_button(self):
        return By.id("login")

    @elements
    def menu_items(self):
        return By.css(".menu-item")


class HomeScreen(MobileScreen):

    @webview(klass=MainWebView)
    def main_webview(self):
        pass
```

---

## Automatic context switching

Hyperion manages webview context transitions transparently:

- Before resolving or interacting with a webview child:
  - Hyperion enters the webview context.
- After the operation:
  - the previous host context is restored automatically.

This applies uniformly to:
- element lookup
- waits
- interactions
- assertions and verifications
- visual checks
- EQL evaluation

---

## Waits and presence

Waiting is performed on the **elements inside** the webview (using standard `Element` / `Elements` waits).

```python
# `screen` is an instance of HomeScreen (created by your test setup)
screen.main_webview.login_button.wait_until_visible()
screen.main_webview.menu_items.wait_until_found()
```

---

## Interacting with elements inside a WebView

All interactions use the standard `Element` API.

```python
# `screen` is an instance of HomeScreen (created by your test setup)
screen.main_webview.login_button.click()
screen.main_webview.menu_items[0].assert_visible()
```

---

## EQL selection inside a WebView

EQL selection works identically inside a webview and is scoped automatically.

```python
# `screen` is an instance of HomeScreen (created by your test setup)
item = screen.main_webview.menu_items['text == "Settings"']
assert item is not None

item.click()
```

EQL evaluation:
- runs inside the webview context
- never leaks into the host or other webviews

---

## Visual assertions inside a WebView

Element-level visual assertions are fully supported.

```python
# `screen` is an instance of HomeScreen (created by your test setup)
screen.main_webview.login_button.assert_visual_match(
    "/tmp/baselines/login_button.png"
)
```

Hyperion ensures the correct webview context before capturing visuals.

---

## Stability and error handling

WebView interactions participate in Hyperion’s global stability model:

- retries on transient lookup failures
- recovery from stale references
- interactive waits instead of passive sleeping

No additional handling is required from the test author.

---

## Practical guidance

- Treat `WebView` as a **page-like root inside a host**.
- Never manage context switching manually.
- Declare webview structure once; interact normally afterward.
- Use EQL inside webviews for semantic, order-independent selection.
- End tests with explicit assertions.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [IFrame](/docs/reference/public-api/iframe.md)  
→ Next: [Element](/docs/reference/public-api/element.md)
