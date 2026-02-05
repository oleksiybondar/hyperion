[← Verify](/docs/reference/public-api/verify.md) | [REST Client →](/docs/reference/public-api/http-client.md)

# Wait API

Hyperion waits are **interactive synchronization primitives**.

They are designed to replace passive sleeping with a model that is:
- **polling-based** (re-checks conditions until satisfied)
- integrated with **retries and recovery**
- **context-safe** (works across widgets / iframes / webviews without manual switching)
- **loggable and debuggable** (wait attempts are traceable through Hyperion logs)

In Hyperion, you typically do not “wait for time”.
You **wait for a condition**.

---

## Core principles

### Waiting is interactive, not sleeping

Avoid:

```python
import time
time.sleep(2)
```

Prefer:

```python
page.submit_button.wait_until_fully_interactable()
page.submit_button.click()
```

### Waits are part of stable interaction

Hyperion waits:
- re-resolve elements as needed
- tolerate transient UI changes (stale references, short DOM mutations)
- keep synchronization declarative and local to the UI object you interact with

---

## Common wait parameters

Element and collection wait methods support the same optional keyword arguments:

- `timeout: float | None = None`  
  Maximum time (seconds) to wait for the condition.

- `raise_exception: bool = False`  
  Controls timeout behavior:
  - when `True`, the wait raises on timeout
  - when `False`, the wait returns `False` on timeout

> These parameters are accepted even when the method signature does not show them explicitly, because waits are implemented as “wait-wrapped” methods.

---

## Return value semantics

Wait methods return `bool`:

- `True` when the condition becomes satisfied within the timeout
- `False` when the timeout expires and `raise_exception=False`

This enables two valid usage styles:

### “Fail-fast” waits (raise on timeout)

```python
page.login_button.wait_until_interactable(timeout=10, raise_exception=True)
page.login_button.click()
```

### Decision-driven waits (do not raise)

```python
if page.spinner.wait_until_missing(timeout=2, raise_exception=False):
    page.results.wait_until_found(raise_exception=True)
else:
    # Explicit test contract still belongs to assertions
    page.error_banner.assert_visible()
```

> Tests must still end with explicit `assert_*` calls for outcomes.

---

## Default timeouts

Wait defaults are provided by Hyperion configuration and used when `timeout` is not specified.

Common defaults used by element/collection waits include:

| Setting | Default |
|---|---:|
| `wait_timeout` | `30` |
| `missing_timeout` | `5` |
| `search_attempts` | `3` |
| `search_retry_timeout` | `0.5` |
| `stale_recovery_timeout` | `0.5` |

The important contract:
- waits are **time-bounded**
- retries and recovery are applied during wait execution

---

## Element waits

Element waits operate on a single `Element`.

### wait_until_found(timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until the element becomes present.

### wait_until_missing(timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until the element is no longer present.

### wait_until_visible(timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until the element becomes visible.

### wait_until_hidden(timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until the element becomes hidden.

### wait_until_enabled(timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until the element becomes enabled.

### wait_until_interactable(timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until the element is ready for user interaction (visible + enabled).

### wait_until_animation_completed(timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until the element’s geometry stabilizes (no ongoing animation).

### wait_until_fully_interactable(timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until the element is:
- visible
- enabled
- animation completed

#### Example: stable click without sleeping

```python
from hyperiontf import WebPage, element, By


class CheckoutPage(WebPage):

    @element
    def place_order(self):
        return By.id("place-order")

    @element
    def confirmation(self):
        return By.id("order-confirmation")


def test_place_order(checkout_page: CheckoutPage):
    checkout_page.place_order.wait_until_fully_interactable(
        timeout=15,
        raise_exception=True,
    )
    checkout_page.place_order.click()

    checkout_page.confirmation.assert_visible()
```

---

## Collection waits (Elements)

Collection waits operate on `Elements` (a list-like collection of `Element` items).

### wait_until_found(timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until at least one item exists.

### wait_until_missing(timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until no items exist.

### wait_until_items_count(expected_count: int, timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until the collection length equals `expected_count`.

### wait_until_items_increase(timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until the collection length increases compared to the previous observation.

### wait_until_items_decrease(timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until the collection length decreases compared to the previous observation.

### wait_until_items_change(timeout: float | None = None, raise_exception: bool = False) -> bool

Wait until the collection length changes (increase or decrease) compared to the previous observation.

#### Example: wait for results to load

```python
from hyperiontf import WebPage, elements, By


class ResultsPage(WebPage):

    @elements
    def rows(self):
        return By.css(".result-row")

    @element
    def empty_state(self):
        return By.id("no-results")


def test_results_load(results_page: ResultsPage):
    found = results_page.rows.wait_until_found(timeout=10)

    if found:
        assert len(results_page.rows) >= 1
        results_page.rows[0].assert_visible()
    else:
        # Explicit outcome check (test contract)
        results_page.empty_state.assert_visible()
```

---

## How to choose a wait

Use the narrowest wait that matches intent:

- “the element exists” → `wait_until_found()`
- “the user can click it” → `wait_until_interactable()` / `wait_until_fully_interactable()`
- “loading finished” → `wait_until_missing()` on spinner
- “the list updated” → `wait_until_items_change()`

Avoid:
- waiting longer “just in case”
- sleeping to cover animations
- mixing waiting and outcome validation

Waits synchronize.  
Assertions validate.

---

## Summary

Hyperion’s Wait API provides:
- interactive, condition-based synchronization
- optional timeout control (`timeout`)
- optional error behavior (`raise_exception`)
- built-in stability via retries and recovery
- consistent behavior across pages, widgets, iframes, and webviews

---

[← Verify](/docs/reference/public-api/verify.md) | [REST Client →](/docs/reference/public-api/http-client.md)