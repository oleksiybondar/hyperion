# 5.1 WebPage

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Component: Table](/docs/how-to/table.md)  
→ Next: [MobileScreen](/docs/reference/public-api/mobilescreen.md)

---

`WebPage` is the root Page Object for **web UI automation** in Hyperion.

Use it to:
- start a browser session
- navigate to a URL
- model UI as a hierarchy of elements/widgets/iframes
- interact with the UI through Hyperion’s stable, logged APIs

---

## Import

```
from hyperiontf import WebPage
```

---

## Starting a browser session

### `WebPage.start_browser(caps: dict | None = None, attempts: int = ...) -> WebPage`

Starts a browser session and returns an instance of your page class.

#### `caps`
`caps` can be:
- `None` (or omitted): use the default configuration
- `dict`: explicitly define capabilities for this session

#### Capabilities keys (web)

`automation`  
Selects the web automation backend.

Supported values:
- `selenium`
- `playwright`

`browser`  
Selects the target browser engine.

Supported values:
- `chrome`
- `firefox`
- `edge`
- `safari`
- `electron`
- `chromium`
- `webkit`
- `remote`

Other keys may be provided (for example `headless`) and will be forwarded to the selected automation backend.

#### Examples

```python
from hyperiontf import WebPage


class ProductPage(WebPage):
    pass


# Selenium examples
firefox_caps = {"automation": "selenium", "browser": "firefox", "headless": True}
chrome_caps = {"automation": "selenium", "browser": "chrome", "headless": True}
edge_caps = {"automation": "selenium", "browser": "edge"}

# Playwright examples
webkit_playwright_caps = {"automation": "playwright", "browser": "webkit"}
chrome_playwright_caps = {"automation": "playwright", "browser": "chrome"}
firefox_playwright_caps = {"automation": "playwright", "browser": "firefox"}


page = ProductPage.start_browser(chrome_caps)
```

---

## Navigation

### `open(url: str) -> None`

Navigates the browser to the given URL.

```python
page.open("http://localhost:8000/product")
```

---

## Page metadata

### `title -> str`

Returns the current page title.

```python
current_title = page.title
```

---

## Viewport

Hyperion models viewport as a first-class concept (used by responsive locators and viewport-aware logic).

### `viewport -> str`

Returns the current viewport label.

Supported values:
- `xs`
- `sm`
- `md`
- `lg`
- `xl`
- `xxl`

### `viewport = <label>`

Sets the current viewport label.

### `change_viewport(width: int, height: int | None = None) -> None`

Resizes the viewport.

```python
label = page.viewport
page.viewport = "sm"
page.change_viewport(width=390, height=844)
```

---

## Platform and OS identity

### `platform -> str`

Always returns `web`.

### `os -> str`

Returns the current OS name (for example: `Windows`, `Darwin`, `Linux`).

---

## Inherited API

`WebPage` inherits common Page Object capabilities.

### `action_builder`

Provides a fluent API for advanced interactions (mouse/keyboard/touch) with full logging.

See: → [/docs/reference/public-api/action-builder.md](/docs/reference/public-api/action-builder.md)

### `quit() -> None`

Closes the session.

### `make_screenshot(filepath: str | None = None)`

Captures a screenshot and returns it as an image object.

### `screenshot(message: str = ..., title: str = ...) -> None`

Captures and attaches a screenshot to the test log.

### Visual helpers

Page objects also provide visual verification helpers such as `verify_visual_match(...)` and `assert_visual_match(...)`.

See: → [/docs/reference/public-api/visual.md](/docs/reference/public-api/visual.md)

---

## Recommended usage pattern

Model UI structure with `@element` / `@widget(s)` and model page behavior with methods.

```python
from hyperiontf import WebPage, element, By


class ProductPage(WebPage):

    @element
    def quantity_input(self):
        return By.id("quantity")

    @element
    def add_to_cart_button(self):
        return By.id("add-to-cart")

    @element
    def confirmation_message(self):
        return By.id("cart-confirmation")

    def add_product_to_cart(self, quantity: int) -> None:
        self.quantity_input.fill(str(quantity))
        self.add_to_cart_button.click()
```

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Component: Table](/docs/how-to/table.md)  
→ Next: [MobileScreen](/docs/reference/public-api/mobilescreen.md)
