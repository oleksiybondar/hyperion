# 3.5 Expect vs Verify

← [/docs/tutorials/iframes-and-context.md](/docs/tutorials/iframes-and-context.md) | [/docs/tutorials/index.md](/docs/tutorials/index.md) →

---

Assertions are one of the most misunderstood parts of test automation.

Most frameworks reduce the discussion to:
- “hard vs soft assertions”
- “fail fast vs continue”

Hyperion takes a different approach.

In Hyperion, the distinction between **expect** and **verify** is not about severity —  
it is about **intent**.

---

## The core idea

> **Assertions answer “is this correct?”**  
> **Verification answers “why did we go down this path?”**

Both are necessary — but they serve different purposes.

---

## Expect: verification of correctness

`expect` (and element-level `assert_*` helpers) are used to verify **test outcomes**.

Characteristics:
- failure raises immediately
- execution stops
- test result is unambiguous
- failure location is explicit

### Example

```python
def test_order_confirmation(checkout_page):
    checkout_page.pay_with_card("4111111111111111")

    checkout_page.confirmation_message.assert_text(
        "Thank you for your order"
    )
```

This is a **verification**:
- the test outcome depends on it
- if it fails, the test is invalid
- there is no meaningful continuation

This should be the **default** at the test level.

---

## Verify: logging decisions, not validating outcomes

`verify` evaluates a condition **without raising**.

Its primary purpose is:
- to record *decisions*
- to explain *branching logic*
- to preserve diagnostic context in logs

A `verify` call logs:
- expected value
- actual value
- difference (when applicable)

Even if execution continues.

---

## Where `verify` shines: decision points

Consider a Page Object that must choose between UI variants.

```python
class ProductPage(WebPage):

    @element
    def feature_marker(self):
        return By.id("feature-flag")

    def proceed(self) -> None:
        if self.feature_marker.verify_text("feature-A"):
            self._feature_a_flow()
        else:
            self._default_flow()
```

What matters here is **not** whether `"feature-A"` is correct.

What matters is:
- *which path was taken*
- *why it was taken*
- *what was observed at the decision point*

If the test later fails, the log still explains:
- what the marker contained
- what was expected
- why a particular branch executed

Without `verify`, that information would be lost.

---

## Verify is not “soft expect”

It is tempting to treat `verify` as a soft assertion and accumulate results:

```python
ok = True
ok &= element.verify_text("A")
ok &= element.verify_text("B")
ok &= element.verify_text("C")

if not ok:
    raise AssertionError("Something failed")
```

This is **technically possible** — but strongly discouraged.

Why?

- the log becomes harder to read
- decision intent is unclear
- the failure context is detached from the assertion
- error reporting becomes implicit instead of explicit

From a debugging perspective, this is a smell.

If multiple conditions must be **true**, use multiple assertions instead.

---

## Prefer explicit expectations for validation

This is clearer:

```python
element.assert_text("A")
element.assert_attribute("state", "enabled")
element.assert_visible()
```

Each assertion:
- clearly states intent
- has its own failure context
- produces readable logs
- fails at the correct location

Assertions are about **correctness**, not control flow.

---

## Verify in tests: allowed, but deliberate

Using `verify` directly in tests is allowed.

But it should be **intentional**, not habitual.

Good reasons:
- conditional execution
- exploratory checks
- logging observed behavior without failing immediately

Bad reasons:
- replacing assertions
- avoiding failures
- accumulating state

As a rule of thumb:

> Tests mostly **assert**.  
> Page Objects mostly **verify**.

---

## Verify and EQL

Elements Query Language (EQL) relies on `verify` internally.

When you write:

```python
card = products['title.text == "Coffee Mug"']
```

Hyperion:
- evaluates each candidate
- verifies matching conditions
- logs why elements matched or didn’t

This makes EQL selection **debuggable**, not magical.

When selection fails, logs explain *why* — not just *that* it failed.

---

## Design guidelines

Use **expect / assert** when:
- validating test outcomes
- checking correctness
- failure must stop execution

Use **verify** when:
- making a decision
- choosing a branch
- selecting among alternatives
- recording observed behavior

Avoid:
- accumulating verify results
- raising manually later
- hiding assertion intent

---

## What You Learned

You now understand:
- why expect and verify are not interchangeable
- how verify enables decision logging
- why assertions should remain explicit
- how logs become more useful with intentional verification

Most importantly:

> **If a condition determines the flow, verify it.**  
> **If a condition determines correctness, assert it.**

---

## End of Tutorials

You’ve completed the Tutorials section.

From here, you can:
- dive into **How-To Guides** for specific problems
- explore **Examples** for real-world patterns
- consult the **API Reference** for authoritative details

← [/docs/index.md](/docs/index.md)