# 3.2 Page Objects 101

← [/docs/tutorials/first-web-test.md](/docs/tutorials/first-web-test.md)

---

In 3.1, you wrote your first Hyperion web test.

In this tutorial, we go one level deeper:
- how to design Page Objects that scale
- how to keep tests readable as the UI grows
- how to prepare your codebase for reusable components

We’ll stay in the same abstract e-commerce domain.

---

## Why Page Objects exist (beyond “grouping elements”)

In Hyperion, Page Objects are not just a place to store locators.

A Page Object is a **facade** that:
- describes page structure (elements)
- exposes page behavior (methods)
- hides implementation details (locators, optional UI, variants)

If you come from modern UI development (React/Vue/server-side templates), you already think in **composable parts**.
You don’t build a giant “page blob” — you assemble it from reusable pieces.

Hyperion encourages the same approach in test automation:
- structured hierarchy
- behavior on the object that owns the elements
- minimal test logic

This approach has an upfront cost (more design), but it pays back by:
- reducing duplicated locators and flows
- improving readability
- making logs self-explanatory (you can “read” the UI interaction path)

---

## The Scenario

We’ll model an abstract product page:

- user sets quantity
- user adds product to cart
- confirmation appears

We will start with a “naive” test and then refactor it into a clean design.

---

## Step 1: The “naive” test (works, but doesn’t scale)

This test directly orchestrates element interactions.

It is fine for one test.
It becomes painful when you write 50 tests.

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401


def test_add_product_to_cart_naive(product_page):
    product_page.quantity_input.fill("2")
    product_page.add_to_cart_button.click()
    product_page.confirmation_message.assert_text("Product added to cart")
```

### What goes wrong over time

- the same 3–6 UI steps get repeated everywhere
- small UI changes create large refactor churn
- tests become “Selenium scripts” with business intent buried in mechanics
- logs show actions, but your test code stops telling a clear story

---

## Step 2: Move behavior into the Page Object

Your test should express *intent*:

- “add product to cart with quantity 2”
- “confirmation should appear”

It should not express *how* the UI does that.

### Page Object (structure + behavior)

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

### Refactored test (intent-driven)

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401


def test_add_product_to_cart(product_page):
    product_page.add_product_to_cart(quantity=2)
    product_page.confirmation_message.assert_text("Product added to cart")
```

Now the test reads like a scenario, not a script.

---

## Step 3: Page methods should accept external data

A good Page Object method:
- accepts external inputs (quantity, promo code, user email)
- knows which elements are required/optional
- encapsulates mechanics and minor UI differences

Example:

```python
class ProductPage(WebPage):

    @element
    def quantity_input(self):
        return By.id("quantity")

    @element
    def add_to_cart_button(self):
        return By.id("add-to-cart")

    def add_product_to_cart(self, quantity: int) -> None:
        self._set_quantity(quantity)
        self.add_to_cart_button.click()

    def _set_quantity(self, quantity: int) -> None:
        self.quantity_input.fill(str(quantity))
```

### Why private helpers matter

Private helpers let you:
- reuse internal flows
- split complex behavior into readable chunks
- keep your public Page API small and stable

This is especially important when the same UI can be rendered in multiple variants
(A/B tests, campaigns, experiment flags).

> Note: In later tutorials, you’ll see how `verify` helps log *decisions* when choosing between variants.
> For now, we keep this tutorial focused on `assert_*` verification.

---

## Step 4: Naming is a feature

A well-designed Page Object is also documentation.

Prefer names that match product language:
- `add_product_to_cart()` instead of `click_add_button()`
- `apply_promo_code()` instead of `fill_input_and_click()`
- `cart_total_amount` instead of `label_3`

This is not cosmetic.

Your logs (and your future debugging self) benefit from a structured model where actions appear as meaningful paths, like:

- `ProductPage.add_product_to_cart(...)`
- `CartPage.checkout_button.click()`
- `CheckoutPage.shipping_form.fill(...)`

This is one reason Hyperion encourages a structured hierarchy: it makes your automation *explain itself* through readable interaction paths and logs.

---

## Step 5: Preparing for composable UI components

Modern pages are not flat.
They are assembled from repeatable components:
- product cards
- navigation bars
- carts
- checkout forms
- payment blocks

In Hyperion, the scalable way to model those is through **nested Page Objects** (widgets and reusable components).

We are not introducing widgets yet (that’s the next tutorial),
but the design rule already applies:

> If you find yourself repeating the same mini-structure across pages,
> it probably wants to become a reusable component.

---

## What You Learned

You now know how to:
- refactor a “script-like” test into an intent-driven test
- place behavior in Page Objects (methods)
- design Page APIs that accept external data
- keep tests readable as the system grows

You also adopted a scalable mental model:

> UI is built from components — your test model should be too.

---

## Next Tutorial

Next, we’ll turn repeated UI structures into reusable components using widgets:

→ [/docs/tutorials/widgets-101.md](/docs/tutorials/widgets-101.md)

---
← [/docs/tutorials/first-web-test.md](/docs/tutorials/first-web-test.md)