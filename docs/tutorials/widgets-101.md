# 3.3 Widgets and Reusable Components

← [/docs/tutorials/page-objects-101.md](/docs/tutorials/page-objects-101.md)

---

Modern user interfaces are not flat.

Whether you build with React, Vue, or server-side rendering, pages are assembled from **reusable components**:
- product cards
- navigation bars
- forms
- banners
- modals

This tutorial shows how to apply the **same compositional mindset** to Hyperion tests using **widgets**.

---

## Why flat Page Objects don’t scale

A common automation approach looks like this:

- one large page class
- dozens of unrelated elements
- duplicated locators across pages
- repeated interaction logic

This usually happens not because engineers prefer flat models — but because **hierarchy is hard to maintain** in traditional automation frameworks.

Typical pain points:
- elements go stale after re-render
- nested structures lose context
- reusable UI parts must be redefined per page
- debugging requires inspecting the DOM, not reading the test

To cope, teams flatten their Page Objects — and pay the price later.

---

## Hyperion’s premise

Hyperion takes a different approach:

> If the framework can guarantee **stability, recovery, and correct reassembly**,  
> then users should be free to model the UI as it actually exists.

That’s what widgets enable.

---

## What is a Widget in Hyperion?

A **Widget** is:
- a reusable, nested Page Object
- a logical UI component
- composed of its own elements and behavior
- attachable to pages *and other widgets*

Conceptually:
- `WebPage` → full screen
- `Widget` → component
- `Element` → leaf node

This mirrors how modern frontends are built.

---

## The Scenario

We continue with the abstract e-commerce application.

The product listing page contains:
- multiple product cards
- each card has:
  - title
  - price
  - “Add to cart” button

Each card behaves the same — only the data differs.

That makes it an ideal widget.

---

## Step 1: Define a reusable Widget

We start by modeling a **ProductCard** component.

```python
from hyperiontf import Widget, element, By


class ProductCard(Widget):

    @element
    def title(self):
        return By.css(".product-title")

    @element
    def price(self):
        return By.css(".product-price")

    @element
    def add_to_cart_button(self):
        return By.css(".add-to-cart")

    def add_to_cart(self) -> None:
        self.add_to_cart_button.click()
```

### Key characteristics

- The widget knows **only about itself**
- It defines both structure and behavior
- It does not care where it is rendered

This is exactly how UI components are designed.

---

## Step 2: Attach widgets to a Page

Now we attach multiple product cards to a page.

```python
from hyperiontf import WebPage, widgets, By
from .product_card import ProductCard


class ProductsPage(WebPage):

    @widgets(klass=ProductCard)
    def products(self):
        return By.css(".product-card")

    @element
    def cart_confirmation(self):
        return By.id("cart-confirmation")
```

### What this gives you

- `products` is an `Elements` collection of `ProductCard`
- each item is fully functional
- indexing reflects UI order
- hierarchy mirrors page structure

---

## Step 3: Use widgets by position

Index-based selection is useful when **order matters**.

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401


def test_add_second_product_to_cart(products_page):
    products_page.products[1].add_to_cart()

    products_page.cart_confirmation.assert_text(
        "Product added to cart"
    )
```

This reads as a UI description:
- page → products list → second card → add to cart

---

## Step 4: Select widgets by meaning (EQL)

In real e-commerce tests, order often does *not* matter.

You usually want:
- “Add **Coffee Mug** to cart”
- not “Add the second product”

Hyperion supports this using **Elements Query Language (EQL)**.

We won’t deep-dive into EQL here — just enough to show the idea.

### Page-level semantic action

```python
class ProductsPage(WebPage):

    @widgets(klass=ProductCard)
    def products(self):
        return By.css(".product-card")

    @element
    def cart_confirmation(self):
        return By.id("cart-confirmation")

    def add_product_to_cart(self, title: str) -> None:
        card = self.products[f'title.text == "{title}"']
        card.add_to_cart()
```

### Test using semantic selection

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401


def test_add_product_by_title(products_page):
    products_page.add_product_to_cart(title="Coffee Mug")

    products_page.cart_confirmation.assert_text(
        "Product added to cart"
    )
```

### Why this matters

- tests become intention-driven
- index brittleness is avoided
- selection attempts are logged, aiding debugging
- hierarchy + semantics work together

---

## Widgets can contain widgets

Real components are rarely flat.

A product card might include:
- a price block
- a badge
- a rating widget

Hyperion supports nested widgets naturally.

```python
from hyperiontf import Widget, element, By


class PriceBlock(Widget):

    @element
    def amount(self):
        return By.css(".amount")

    @element
    def currency(self):
        return By.css(".currency")
```

```python
from hyperiontf import widget


class ProductCard(Widget):

    @widget(klass=PriceBlock)
    def price(self):
        return By.css(".price")
```

Hierarchy stays explicit and readable.

---

## Why hierarchy is a feature

A structured widget hierarchy gives you:

1. **Readability**  
   Tests describe the UI without exposing DOM details.

2. **Reuse**  
   The same widget can appear on multiple pages without duplication.

3. **Debuggability**  
   Logs reflect object paths, not raw selectors.

Hyperion’s recovery and reassembly guarantees make this approach safe.

---

## Design rule of thumb

If you find yourself:
- copying the same locators across pages
- repeating the same interaction logic
- mentally grouping elements into a “thing”

That “thing” wants to be a widget.

---

## What You Learned

You now know:
- why flat Page Objects don’t scale
- how widgets enable safe composition
- how hierarchy improves readability and reuse
- how to select widgets by position or by meaning

Most importantly:

> Tests should model **what the user sees**,  
> not what the DOM happens to look like today.

---

## Next Tutorial

Next, we’ll apply the same model to one of the hardest UI challenges:
**iFrames and context switching**, without manual context management.

→ [/docs/tutorials/iframes-and-context.md](/docs/tutorials/iframes-and-context.md)

---
← [/docs/tutorials/page-objects-101.md](/docs/tutorials/page-objects-101.md)