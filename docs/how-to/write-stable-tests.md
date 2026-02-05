← [Back to Documentation Index](/docs/index.md)  
← Previous: [Expect vs Verify](/docs/tutorials/expect-vs-verify.md)  
→ Next: [Wait API and Timeouts](/docs/how-to/handle-waits-and-timeouts.md)

---

# 4.1 Writing Stable Tests

This guide explains **how to write stable tests in Hyperion** by relying on **framework guarantees** instead of defensive test code.

Stability in Hyperion is not achieved by adding sleeps, retries, or exception handling in tests.  
It is achieved by **expressing intent clearly** and letting the framework handle synchronization, retries, and recovery.

---

## What “stable” means in Hyperion

A stable test is one that:

- behaves deterministically across environments
- survives transient UI states (animations, re-renders, delays)
- fails only on **real errors**, not timing artifacts
- produces logs that explain *why* a failure happened

Stability is a **framework concern**, not a test concern.

Your job as a test author is to describe *what should happen*, not *how long to wait*.

---

## Core principle: express intent, not timing

Unstable tests usually encode timing assumptions:

- “wait 2 seconds”
- “retry this click”
- “catch exception and try again”

These approaches are fragile because they guess about runtime behavior.

In Hyperion:

- waiting is **interactive**, not passive
- retries are **automatic**
- stale recovery is **scope-preserving**
- context switching is **automatic**

Tests should not reimplement these mechanisms.

---

## Do not use sleeps to stabilize tests

Avoid using `time.sleep(...)` to “wait for the UI”.

Why this is harmful:

- sleeps assume a fixed timing that may not hold
- they slow down fast environments
- they still fail in slow or unstable environments
- they hide real synchronization issues

Hyperion already retries element resolution and interaction under observable conditions.  
Adding sleeps on top reduces reliability rather than improving it.

> The only acceptable use of sleeps is **demo pacing or debugging**, never test stabilization.

---

## Let retries and recovery do their job

Hyperion automatically retries:

- element resolution
- interactions
- stale-element scenarios

Retries are:

- bounded
- configurable
- exponential with Page Object depth
- performed within the correct context and scope

Because of this, tests should **not**:

- wrap actions in try/except to retry
- catch stale element exceptions
- loop until something “works”

If an operation ultimately fails, it is a real failure that should surface.

---

## Keep tests short and intention-focused

A good test:

- reads like a scenario
- contains no platform logic
- ends with explicit assertions

Example structure:

```python
def test_calculation(page):
    page.evaluate_expression(5.6, "+", 10.4)
    result = page.get_result()
    expect(result).to_be(16)
```

Key characteristics:

- no branching on platform or OS
- no timing logic
- assertion happens at the end

---

## Put waiting logic in the right place

If something requires waiting, it should live in:

- a **widget method**, or
- a **Page Object method**

Never in the test itself.

Why:

- widgets and pages understand *what “ready” means*
- tests should not know internal UI readiness conditions
- reuse becomes possible

Example pattern (conceptual):

```python
class ResultsTable:
    def wait_until_ready(self):
        # waits until rows are present and stable
        ...
```

Tests call behavior; widgets encode readiness.

---

## Assert final state, not intermediate steps

Tests should assert **outcomes**, not transitions.

Good assertions:

- final result value
- final UI state
- final count or status

Avoid asserting:

- intermediate animations
- transient loading states
- momentary visibility changes

This keeps tests robust against UI implementation changes.

---

## `expect(...)` vs `verify(...)`

Hyperion distinguishes clearly between assertions and diagnostics.

### `expect(...)`

- represents a **test assertion**
- failure fails the test
- logs full comparison details

### `verify(...)`

- used for **decision logging**
- never fails a test
- explains *why* a branch was taken

Rule of thumb:

- tests end with `expect(...)`
- `verify(...)` may appear inside flows for observability

Do not treat `verify(...)` as a “soft assertion”.

---

## Avoid branching in tests

Tests should not branch on:

- platform
- OS
- viewport
- context type

Branching belongs in:

- Page Objects
- widgets
- locator mappings

This is what allows one test flow to run across web, mobile, desktop, and hybrid contexts unchanged.

---

## Trust the framework contracts

Stable tests are possible because Hyperion guarantees:

- deterministic locator resolution
- automatic context switching
- bounded retries and recovery
- structured logging for diagnosis

These guarantees are defined in:

- `/docs/reference/behavior-contracts/locator-resolution.md`
- `/docs/reference/behavior-contracts/context-switching.md`
- `/docs/reference/behavior-contracts/timeouts.md`

If a test feels unstable, the fix is usually **in the Page Object or widget**, not the test.

---

## Checklist: is your test stable?

Before committing a test, ask:

- Does it avoid sleeps?
- Does it avoid retries in test code?
- Does it avoid platform/OS branching?
- Does it assert only final state?
- Does it rely on Page Object behavior, not element mechanics?

If yes, the test is aligned with Hyperion’s stability model.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Expect vs Verify](/docs/tutorials/expect-vs-verify.md)  
→ Next: [Wait API and Timeouts](/docs/how-to/handle-waits-and-timeouts.md)
