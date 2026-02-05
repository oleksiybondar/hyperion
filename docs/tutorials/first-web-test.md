# 3.1 Your First Web Test

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Stale Element Recovery and Retries](/docs/core-concepts/retry-and-recovery.md)  
→ Next: [Page Objects 101](/docs/tutorials/page-objects-101.md)

---

In this tutorial, you will write your **first meaningful web test** using Hyperion.

We will work with an **abstract e-commerce application** to keep examples realistic while remaining framework-focused.

You will learn how to:
- model a page using Hyperion Page Objects
- describe page behavior using methods
- write a clean, intention-focused test
- validate outcomes using assertions

This tutorial intentionally avoids advanced topics.  
The goal is to establish the **correct mental model** from the start.

---

## The Scenario

Imagine a simple e-commerce product page:

- a product title is displayed
- the user enters a quantity
- the user adds the product to the cart
- the page confirms the action

We will automate this flow.

---

## Step 1: Define the Page Object

In Hyperion, a Page Object represents **both structure and behavior**.

It:
- knows all elements on the page
- knows how those elements work together
- exposes **intent-level methods** to tests

```python
from hyperiontf import WebPage, element, By


class ProductPage(WebPage):

    @element
    def product_title(self):
        return By.id("product-title")

    @element
    def quantity_input(self):
        return By.id("quantity")

    @element
    def add_to_cart_button(self):
        return By.id("add-to-cart")

    @element
    def confirmation_message(self):
        return By.id("cart-confirmation")

    def add_product_to_cart(self, quantity: int):
        self.quantity_input.fill(str(quantity))
        self.add_to_cart_button.click()
```

### Important points

- Elements describe **what exists**
- Methods describe **what the user does**
- Tests should prefer calling methods over orchestrating elements

This is not just grouping — this is **encapsulation of page behavior**.

---

## Step 2: Create a pytest Fixture

Tests should not care about:
- browser startup
- teardown
- logging
- recovery

That belongs in fixtures.

Before writing the test, one required import must be present.

Hyperion integrates with pytest through a lightweight test-case setup hook.
Importing it ensures that:
- each test case produces its own HTML log
- failures and retries are isolated per test
- execution context is correctly reset

The import may appear unused, but it is required.

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401
from hyperiontf.executors.pytest import fixture
from .pages.product_page import ProductPage


@fixture(scope="function", log=False)
def product_page():
    page = ProductPage.start_browser("chrome")
    page.open("http://localhost:8000/product")
    yield page
    page.quit()
```

### Why this matters

- `start_browser()` initializes Hyperion’s execution context
- `open()` navigates to the page
- `quit()` guarantees cleanup even on failure

The test remains focused on **business intent**.

---

## Step 3: Write the Test

Now we express the behavior we want to validate.

```
def test_add_product_to_cart(product_page):
    product_page.add_product_to_cart(quantity=2)

    product_page.confirmation_message.assert_text(
        "Product added to cart"
    )
```

### What you did *not* write

- no explicit waits
- no retries
- no stale handling
- no driver calls

Hyperion handles those concerns automatically.

---

## Step 4: Assertions and Test Validity

The test uses `assert_text`.

This is a **hard assertion**:
- if it fails, the test stops immediately
- execution does not continue in an invalid state
- the failure is clearly reported

This is the correct default for **verification**.

Later tutorials will introduce `verify` for a different purpose:
- recording decisions
- logging branching logic
- preserving diagnostic context

For now, assertions are enough.

---

## What You Learned

You now know how to:
- model a page using Hyperion
- express page behavior using methods
- write a readable, intention-driven test
- validate outcomes correctly

More importantly, you’ve applied the core rule:

> Tests describe **what should happen**.  
> Page Objects describe **how the page behaves**.  
> Hyperion handles **how it is executed**.

---

## Next Tutorial

Next, we will improve this design by:
- moving more logic into Page Objects
- reducing duplication across tests
- making test code even more expressive

Next, we’ll refactor tests to rely entirely on Page Object behavior and APIs:

→ [/docs/tutorials/page-objects-101.md](/docs/tutorials/page-objects-101.md)

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Stale Element Recovery and Retries](/docs/core-concepts/retry-and-recovery.md)  
→ Next: [Page Objects 101](/docs/tutorials/page-objects-101.md)
