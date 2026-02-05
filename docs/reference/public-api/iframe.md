[← Elements](/docs/reference/public-api/elements.md) | [WebView →](/docs/reference/public-api/webview.md)

# IFrame

`IFrame` represents a **structural container whose content lives in a separate browsing context**.

- It behaves like a `Widget` in terms of structure and declaration.
- It reuses the full `Element` API for interaction, waits, assertions, and verifications.
- Its defining feature is **automatic context switching**.

> You never switch context manually.  
> Hyperion guarantees that element resolution and interaction always occur in the correct iframe context.

---

## Conceptual role

| Aspect | Meaning |
|---|---|
| Structural container | Yes |
| Hierarchical | Yes |
| Leaf | No |
| Interaction API | Reuses `Element` |
| Context boundary | Yes |

An `IFrame` defines a **context boundary** in the UI hierarchy:
- All children of the iframe are resolved *inside* the iframe context.
- Parent and sibling elements remain resolved in their original context.

---

## Declaring an iframe

An iframe is declared similarly to a `Widget`, using a locator that identifies the iframe element itself.

```python
from hyperiontf import WebPage, IFrame, iframe, element, By


class PaymentFrame(IFrame):

    @element
    def card_number(self):
        return By.id("card-number")

    @element
    def submit_btn(self):
        return By.id("submit")


class CheckoutPage(WebPage):

    @iframe(klass=PaymentFrame)
    def payment_frame(self):
        return By.css("iframe#payment")
```

- The locator identifies the iframe element in the parent context.
- All children declared under `payment_frame` are automatically scoped to the iframe content.

---

## Declaring children inside an iframe

Children of an `IFrame` are declared the same way as for a `Widget`.

```python
from hyperiontf import WebPage, IFrame, iframe, element, By


class PaymentFrame(IFrame):

    @element
    def card_number(self):
        return By.id("card-number")

    @element
    def submit_btn(self):
        return By.id("submit")


class CheckoutPage(WebPage):

    @iframe(klass=PaymentFrame)
    def payment_frame(self):
        return By.css("iframe#payment")
```

> No manual context switching is required when interacting with `card_number` or `submit_btn`.

---

## Automatic context switching

Hyperion handles iframe context switching **transparently**:

- Before resolving or interacting with an iframe child:
  - Hyperion switches into the iframe context.
- After the operation completes:
  - Hyperion restores the previous context automatically.

This applies to:
- element lookup
- waits
- interactions
- assertions
- visual checks
- EQL resolution

### Nested iframes

Nested iframes are supported naturally.

```python
from hyperiontf import WebPage, IFrame, iframe, element, By


class InnerFrame(IFrame):

    @element
    def button(self):
        return By.id("confirm")


class OuterFrame(IFrame):

    @iframe(klass=InnerFrame)
    def inner(self):
        return By.css("iframe#inner")


class Page(WebPage):

    @iframe(klass=OuterFrame)
    def outer(self):
        return By.css("iframe#outer")
```

Hyperion ensures the correct nesting order when resolving `button`.

---

## Waits and presence

An `IFrame` supports the same presence and wait semantics as other structural objects.

| Method | Meaning |
|---|---|
| `wait_until_found()` | iframe element becomes present |
| `wait_until_missing()` | iframe element becomes absent |
| `is_present` | whether the iframe exists in the current page |

Waiting on an iframe:
- applies to the iframe element itself (in the parent context)
- does **not** implicitly wait for children unless you do so explicitly

```python
from hyperiontf import WebPage, IFrame, iframe, element, By


class PaymentFrame(IFrame):

    @element
    def card_number(self):
        return By.id("card-number")


class CheckoutPage(WebPage):

    @iframe(klass=PaymentFrame)
    def payment_frame(self):
        return By.css("iframe#payment")


page = CheckoutPage.start_browser("chrome")
page.open("https://example.test/checkout")

page.payment_frame.wait_until_found()
page.payment_frame.card_number.wait_until_visible()
```

---

## Using Element and Elements APIs inside an iframe

All child elements behave exactly like regular `Element` or `Elements` instances.

### Example: interaction inside an iframe

```python
from hyperiontf import WebPage, IFrame, iframe, element, By


class PaymentFrame(IFrame):

    @element
    def card_number(self):
        return By.id("card-number")

    @element
    def submit_btn(self):
        return By.id("submit")


class CheckoutPage(WebPage):

    @iframe(klass=PaymentFrame)
    def payment_frame(self):
        return By.css("iframe#payment")


page = CheckoutPage.start_browser("chrome")
page.open("https://example.test/checkout")

page.payment_frame.card_number.clear_and_fill("4242424242424242")
page.payment_frame.submit_btn.click()
```

### Example: EQL selection inside an iframe

```python
from hyperiontf import WebPage, IFrame, iframe, elements, By


class PaymentFrame(IFrame):

    @elements
    def options(self):
        return By.css(".card-option")


class CheckoutPage(WebPage):

    @iframe(klass=PaymentFrame)
    def payment_frame(self):
        return By.css("iframe#payment")


page = CheckoutPage.start_browser("chrome")
page.open("https://example.test/checkout")

row = page.payment_frame.options['text == "Visa"']
assert row is not None

row.click()
```

EQL evaluation is:
- scoped to the iframe
- context-aware
- independent from parent page elements

---

## Visual assertions inside an iframe

Element-level visual assertions work inside iframes without special handling.

```python
from hyperiontf import WebPage, IFrame, iframe, element, By


class PaymentFrame(IFrame):

    @element
    def submit_btn(self):
        return By.id("submit")


class CheckoutPage(WebPage):

    @iframe(klass=PaymentFrame)
    def payment_frame(self):
        return By.css("iframe#payment")


page = CheckoutPage.start_browser("chrome")
page.open("https://example.test/checkout")

page.payment_frame.submit_btn.assert_visual_match(
    "/tmp/baselines/submit_button.png"
)
```

The correct iframe context is entered automatically before the screenshot is taken.

---

## Error handling and stability guarantees

Iframe interactions participate fully in Hyperion’s stability model:

- retries on transient lookup failures
- recovery from stale references
- interactive waits instead of passive sleeping

From a test author’s perspective, iframe interactions are **no different** from regular widget interactions.

---

## Practical guidance

- Treat `IFrame` as a **Widget with a context boundary**.
- Never switch context manually.
- Declare iframe structure once, then interact with children normally.
- Use EQL inside iframes to avoid brittle index-based selection.
- End tests with explicit assertions.

---

[← Elements](/docs/reference/public-api/elements.md) | [WebView →](/docs/reference/public-api/webview.md)