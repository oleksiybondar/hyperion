# 3.4 Working with iFrames

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Widgets and Reusable Components](/docs/tutorials/widgets-101.md)  
→ Next: [Expect vs Verify](/docs/tutorials/expect-vs-verify.md)

---

iFrames are one of the most problematic areas in UI automation.

In most frameworks, they require:
- explicit context switching
- manual “switch back” logic
- defensive code around stale frames
- deep knowledge of browser internals

Hyperion takes a different approach.

In this tutorial, you’ll learn how to work with **single and nested iFrames** using the same compositional model you already use for widgets — **without manual context management**.

---

## The guiding rule

> If you feel the need to call `switch_to_frame` in a test,  
> it is almost always a design problem — not a framework limitation.

In Hyperion, **context switching is a framework concern**, not a test concern.

---

## How Hyperion thinks about iFrames

Conceptually, an iFrame in Hyperion:

- is a real object, not a proxy
- behaves similarly to a widget in the POM hierarchy
- represents a **document boundary**
- requires context switching — but **not by the user**

An iFrame element acts as **two things at once**:
1. a DOM element in the parent document
2. a document root for its children

Accessing children automatically:
- substitutes the active document root
- switches context synchronously

Interacting with parent elements automatically:
- restores the parent document context

From the user’s perspective, all references coexist safely.

---

## The Scenario

We continue with the abstract e-commerce application.

During checkout:
- payment details are hosted in a third-party iframe
- the card number field lives in a nested secure iframe
- confirmation happens back on the main page

This is a very common real-world structure.

---

## Step 1: Define the innermost iFrame

We start with the **secure card entry frame**.

```python
from hyperiontf import IFrame, element, By


class CardNumberFrame(IFrame):

    @element
    def card_number_input(self):
        return By.id("card-number")

    def enter_card_number(self, number: str) -> None:
        self.card_number_input.fill(number)
```

This frame:
- represents a document boundary
- owns its own elements
- exposes intent-level behavior

---

## Step 2: Define the outer payment iFrame

The payment provider iframe contains the secure card frame.

```python
from hyperiontf import IFrame, iframe, element, By
from .card_number_frame import CardNumberFrame


class PaymentFrame(IFrame):

    @iframe(klass=CardNumberFrame)
    def card_number_frame(self):
        return By.id("card-frame")

    @element
    def pay_button(self):
        return By.id("pay")

    def submit_payment(self, card_number: str) -> None:
        self.card_number_frame.enter_card_number(card_number)
        self.pay_button.click()
```

### What happens here

- accessing `card_number_frame` switches context automatically
- entering the card number happens inside the nested iframe
- clicking `pay_button` happens in the payment iframe
- no context management appears in user code

---

## Step 3: Attach the iFrame to the Checkout Page

Now we attach the payment iframe to the page.

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

    def pay_with_card(self, card_number: str) -> None:
        self.payment_frame.submit_payment(card_number)
```

---

## Step 4: Use nested iFrames in a test

Now look at the test.

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401


def test_successful_payment(checkout_page):
    checkout_page.pay_with_card("4111111111111111")

    checkout_page.confirmation_message.assert_text(
        "Thank you for your order"
    )
```

### What you did *not* write

- no `switch_to_frame`
- no `switch_to_default_content`
- no frame bookkeeping
- no defensive recovery logic

Yet:
- nested frames were entered
- contexts were switched
- execution remained synchronous and deterministic

---

## Nested iFrames are not a special case

From the Page Object perspective:

- a page contains an iframe
- an iframe contains another iframe
- each level defines its own structure and behavior

This mirrors how modern UIs are built:
- components nested inside components
- each with its own responsibility
- runtime manages actual DOM attachment

Hyperion applies the same idea to browser context.

---

## Why this works safely

Hyperion guarantees that:
- iframe context switching is transparent
- document roots are substituted correctly
- references remain valid across re-renders
- context is restored automatically after interactions

From the test author’s perspective:
- objects are real
- calls are synchronous
- hierarchy is stable

---

## Design rule of thumb

If your test:
- explicitly switches context
- tracks which frame is “active”
- manually switches back to the page

Then the Page Object model is leaking browser concerns.

In Hyperion, **the hierarchy should express the structure** —
and the framework handles the mechanics.

---

## What You Learned

You now know:
- how Hyperion models iFrames
- how nested iFrames are composed safely
- why context switching is implicit
- how iFrames fit naturally into the widget hierarchy

Most importantly:

> iFrames are not an exception —  
> they are just another structural boundary.

---

## Next Tutorial

Next, we’ll look at a subtle but critical distinction:
**Expect vs Verify** — verification versus decision logging.

→ [/docs/tutorials/expect-vs-verify.md](/docs/tutorials/expect-vs-verify.md)

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Widgets and Reusable Components](/docs/tutorials/widgets-101.md)  
→ Next: [Expect vs Verify](/docs/tutorials/expect-vs-verify.md)
