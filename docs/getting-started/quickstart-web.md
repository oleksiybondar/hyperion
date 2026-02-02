← [Back to Documentation Index](/docs/index.md)  
→ Next: [Quickstart: API Testing](/docs/getting-started/quickstart-api.md)

---

# 1.4 Quickstart: Web UI Testing

This Quickstart shows a minimal, end-to-end **Web UI test** using Hyperion’s Page Object Model, including a **nested iframe** flow — a very common pattern in real checkout and payment integrations.

The goal is not to explain every feature, but to show Hyperion working end-to-end in a realistic scenario.

You will:
- Define a page object with a **nested iframe structure**
- Interact with elements inside the **inner iframe**
- Execute a simple checkout confirmation
- Use **`expect`** and **`verify`** for basic assertions

---

## Minimal setup

This example assumes you already completed:

- [1.1 Installation](/docs/getting-started/installation.md)
- [1.2 Project Setup (pytest)](/docs/getting-started/project-setup-pytest.md)
- [1.3 Basic Configuration](/docs/getting-started/configuration.md)

No special configuration is required for this example beyond starting a browser and opening a page.

---

## Page Objects

In this example, we model a checkout page that embeds a **payment provider iframe**, which itself embeds a **hosted card form iframe**.

Page objects in Hyperion are declared using decorators such as `@element` and `@iframe`.  
Although the decorated methods return **locators**, Hyperion replaces them at runtime with rich objects (for example `Element` or `IFrame`) that expose behavior like `click()`, `fill()`, and assertions.

---

### Inner iframe: hosted card form

This class represents the **innermost iframe**, typically used by payment providers to host sensitive fields such as card numbers.

Even though the methods return locators, accessing `card_number` or `submit` later will yield fully functional element objects, not raw locators.

```python
from hyperiontf import IFrame, By, element


class CardFormFrame(IFrame):
    """
    Inner iframe containing hosted payment fields.
    """

    @element
    def card_number(self):
        # Locator for the card number input inside the iframe
        return By.css("#card-number")

    @element
    def submit(self):
        # Locator for submitting the payment form
        return By.css("#submit-payment")
```

---

### Outer iframe: payment provider

This iframe represents the **payment provider container**, which embeds the hosted card form iframe.

The nesting mirrors the real DOM structure: the checkout page embeds the provider iframe, and the provider iframe embeds the card form iframe.

```python
from hyperiontf import IFrame, By, iframe


class PaymentProviderFrame(IFrame):
    """
    Outer iframe provided by the payment provider.
    """

    @iframe(klass=CardFormFrame)
    def card_form(self):
        # Locator for the inner iframe element
        return By.css("iframe.card-form")
```

---

### Checkout page

The checkout page is the top-level page object.  
It embeds the payment provider iframe and exposes a confirmation element used to verify the result of the checkout.

```python
from hyperiontf import WebPage, By, element, iframe


class CheckoutPage(WebPage):
    """
    Checkout page embedding a payment provider iframe.
    """

    @element
    def page_title(self):
        return By.css("h1")

    @iframe(klass=PaymentProviderFrame)
    def payment(self):
        # Outer payment provider iframe
        return By.css("iframe.payment-provider")

    @element
    def confirmation_message(self):
        # Displayed after a successful payment
        return By.css(".payment-confirmation")
```

---

## The test

The test below exercises the **entire nested iframe flow**.

Notice that:
- No iframe context switching is written explicitly
- No waits or retries are defined
- The test code reads as if all elements were on a single page

Hyperion handles context switching and synchronization automatically based on the page object structure.

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401
from hyperiontf.executors.pytest import fixture
from hyperiontf import expect, verify


@fixture(scope="function")
def checkout_page():
    page = CheckoutPage.start_browser("chrome")
    page.open("https://example.test/checkout")
    yield page
    page.quit()


def test_checkout_with_embedded_payment(checkout_page):
    # Sanity check on the main page
    expect(checkout_page.page_title).to_have_text("Checkout")

    # Interact with elements inside a nested iframe
    checkout_page.payment.card_form.card_number.fill("4111111111111111")
    checkout_page.payment.card_form.submit.click()

    # Critical assertion: payment completed
    expect(checkout_page.confirmation_message).to_be_visible()

    # Non-fatal verification example
    verify(checkout_page.confirmation_message).to_have_text("Payment successful")
```

---

## What just happened

- You interacted with elements inside a **nested iframe** without switching context manually.
- The iframe hierarchy was declared structurally in the Page Object Model.
- Element lookup, context switching, and synchronization were handled by the framework.
- Assertions were expressed using Hyperion’s **`expect`** and **`verify`** APIs.

---

## What this already demonstrates

Without additional configuration, this Quickstart exercised:

- Hierarchical Page Object Model
- Structural nesting via iframes
- Automatic context switching
- Framework-managed synchronization and recovery
- Clear assertion semantics (`expect` vs `verify`)

---

← [Back to Documentation Index](/docs/index.md)  
→ Next: [Quickstart: API Testing](/docs/getting-started/quickstart-api.md)