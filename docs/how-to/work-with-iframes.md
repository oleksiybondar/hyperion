# 4.8 Working with iFrames

← [/docs/how-to/nested-widgets.md](/docs/how-to/nested-widgets.md)

---

iFrames are often treated as a special, fragile case in UI automation.

In most frameworks, they force test authors to:
- switch context manually
- track which frame is “active”
- recover from stale frame references
- spread iframe logic across tests

Hyperion intentionally removes these concerns.

This guide explains **how to structure code that works with iFrames safely and idiomatically** in Hyperion.

---

## Mental model: iFrame as a virtual DOM boundary

In Hyperion, an iFrame is:

- a **real Python object**
- part of the Page Object hierarchy
- a structural boundary between documents
- both:
  - a DOM element in the parent document
  - a document root for its children

Accessing children of an iFrame automatically:
- substitutes the active document root
- switches context synchronously

Returning to parent-level elements automatically restores the parent context.

From the user’s perspective, **all objects coexist safely**.

---

## Important consequence: caching iFrame references is safe

Unlike traditional automation frameworks, **caching an iFrame object in a variable is fully supported**.

Example:

```python
payment = checkout_page.payment_frame
payment.submit_payment("4111111111111111")
```

This works correctly because:

- Page Objects, Widgets, and iFrames represent a **virtual structure**
- Parent relationships are preserved
- When the DOM changes:
  - internal automation handles (e.g. Selenium elements) are recreated
  - Python object references remain valid

This is intentional and fundamental to Hyperion’s design.

> **Structure is stable. Execution details are replaceable.**

---

## What is *not* safe (and why)

The real design smells are not about caching —  
they are about **leaking execution mechanics** into test code.

Avoid:

- explicit calls to `switch_to_frame`
- tracking “current frame” state
- splitting iframe logic between page objects and tests
- treating an iframe as a “mode” instead of a component

If a test knows *when* context switches happen,  
the Page Object model is leaking browser concerns.

---

## The Scenario

We continue with the abstract checkout flow.

Structure:
- Checkout page
- Payment provider iframe
- Nested secure iframe for card input

```
CheckoutPage
 └── PaymentFrame
      └── CardDetailsFrame
```

---

## Step 1: Define the innermost iFrame

This frame owns the secure card fields.

```python
from hyperiontf import IFrame, element, By


class CardDetailsFrame(IFrame):

    @element
    def card_number(self):
        return By.id("card-number")

    @element
    def expiry_date(self):
        return By.id("expiry")

    def enter_card_details(self, number: str, expiry: str) -> None:
        self.card_number.fill(number)
        self.expiry_date.fill(expiry)
```

Responsibilities:
- knows its own structure
- exposes intent-level behavior
- no awareness of parent context

---

## Step 2: Define the outer payment iFrame

This frame owns submission behavior.

```python
from hyperiontf import IFrame, iframe, element, By
from .card_details_frame import CardDetailsFrame


class PaymentFrame(IFrame):

    @iframe(klass=CardDetailsFrame)
    def card_details(self):
        return By.id("secure-card-frame")

    @element
    def submit_button(self):
        return By.id("submit-payment")

    def submit_payment(self, number: str, expiry: str) -> None:
        self.card_details.enter_card_details(number, expiry)
        self.submit_button.click()
```

Key points:
- nested iframe access is declarative
- context switching is implicit
- behavior remains cohesive

---

## Step 3: Attach the iFrame to the page

```python
from hyperiontf import WebPage, iframe, element, By
from .payment_frame import PaymentFrame


class CheckoutPage(WebPage):

    @iframe(klass=PaymentFrame)
    def payment_frame(self):
        return By.id("payment-provider")

    @element
    def confirmation_message(self):
        return By.id("order-confirmation")

    def pay_with_card(self, number: str, expiry: str) -> None:
        self.payment_frame.submit_payment(number, expiry)
```

The page:
- exposes a single intent-level method
- does not leak iframe mechanics
- remains readable and stable

---

## Step 4: Use iFrames in a test

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401


def test_successful_payment(checkout_page):
    checkout_page.pay_with_card(
        number="4111111111111111",
        expiry="12/26",
    )

    checkout_page.confirmation_message.assert_text(
        "Thank you for your order"
    )
```

Notice what’s missing:
- no manual context switching
- no frame bookkeeping
- no defensive logic

Yet nested iFrames are handled correctly.

---

## Where iframe logic belongs

A useful rule:

- **Tests** describe business intent
- **Pages / iFrames** describe structure and behavior
- **Framework** handles execution details

If iframe-specific logic appears in tests,  
the abstraction boundary is broken.

---

## iFrames vs Widgets (quick comparison)

| Concept     | Widget                     | iFrame                                  |
|------------|----------------------------|------------------------------------------|
| Purpose    | Logical UI component       | Document boundary                         |
| Context    | Same document              | Separate document                         |
| Structure | Nested hierarchy            | Nested hierarchy                          |
| Switching | Not required                | Automatic and implicit                    |
| Caching   | Safe                        | Safe                                     |

They are different — but they compose the same way.

---

## Design checklist

When working with iFrames, ask:

- Is iframe logic encapsulated in a class?
- Does the test avoid execution details?
- Are behaviors exposed as methods?
- Is caching used freely but responsibly?

If yes — the design is correct.

---

## What You Learned

You now know:
- how Hyperion models iFrames structurally
- why caching iframe references is safe
- how nested iFrames compose naturally
- what patterns to avoid (and why)

Most importantly:

> **iFrames are not special cases.  
> They are structural boundaries — and should be treated as such.**

---

## Next Guides

Continue with:
- [/docs/how-to/work-with-webviews.md](/docs/how-to/work-with-webviews.md)
- [/docs/how-to/eql-recipes.md](/docs/how-to/eql-recipes.md)

---
← [/docs/how-to/nested-widgets.md](/docs/how-to/nested-widgets.md)