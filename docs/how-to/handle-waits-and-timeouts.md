← [Back to Documentation Index](/docs/index.md)  
← Previous: [Writing Stable Tests](/docs/how-to/write-stable-tests.md)  
→ Next: [Handling Animations and Dynamic Content](/docs/how-to/handle-animations.md)

---

# 4.2 Wait API and Timeouts

This guide explains **how waiting and timeouts work in Hyperion**, and how test authors should reason about them.

In Hyperion, waiting is **not an explicit API that tests call**.  
It is a **framework-level behavior** driven by configuration and applied automatically during execution.

---

## Waiting is a framework responsibility

Hyperion treats synchronization as a **core execution concern**, not something test authors should manage manually.

As a result:

- tests do not “wait”
- Page Objects do not “sleep”
- widgets do not poll with loops
- the framework retries and waits automatically under bounded timeouts

Waiting happens implicitly as part of:

- element resolution
- element interaction
- stale element recovery
- context re-selection

---

## Timeouts are configuration-driven

All waiting and retry behavior in Hyperion is controlled via **framework configuration**.

Key properties:

- configuration is **global and singleton**
- configuration is loaded once
- all parts of the framework read from the same configuration state
- test code does not need to pass timeout values around

This ensures consistent behavior across:

- tests
- Page Objects
- widgets
- retries
- recovery logic

---

## What timeouts mean in Hyperion

Timeouts in Hyperion define **how long the framework will keep trying to make progress**, not how long it will pause.

Important characteristics:

- waiting is **interactive**, not passive
- actions are re-attempted under observable conditions
- retries are bounded by timeout values
- execution proceeds as soon as progress is possible

Timeouts do **not**:

- guarantee a fixed delay
- act as sleeps
- represent expected performance

They represent **maximum tolerance for instability**.

---

## Where waiting actually happens

Waiting is automatically applied during:

- element lookup (search + retry)
- interaction attempts (click, fill, etc.)
- stale element recovery
- re-resolution from parent scope
- context verification and switching

From the test author’s perspective, this is transparent.

Tests simply call behavior:

```python
page.evaluate_expression(5.6, "+", 10.4)
result = page.get_result()
expect(result).to_be(16)
```

Any waiting required to make those operations succeed happens inside the framework.

---

## Missing vs slow elements

Hyperion distinguishes between two cases:

- **slow elements**  
  Elements that appear after some time (e.g. due to rendering, network, animation)

- **missing elements**  
  Elements that never appear

This distinction affects:

- how long Hyperion retries
- how failures are reported
- what diagnostics appear in logs

Test code does not need to handle this distinction manually — it exists to improve recovery and observability.

---

## Where to encode readiness logic

If a particular UI feature requires a specific notion of “ready”, that logic belongs in:

- a **widget method**, or
- a **Page Object method**

Never in the test.

Conceptual example:

```python
class ResultsTable:
    def wait_until_ready(self):
        # wait until rows are present and stable
        ...
```

The test calls `wait_until_ready()` as a semantic operation, not as a timing hack.

---

## Do not “tune” timeouts to fix flakiness

Adjusting timeouts should be a **last resort**.

If a test is flaky, the usual causes are:

- missing readiness logic in a widget
- incorrect locator resolution
- relying on intermediate UI states
- asserting too early

Increasing timeouts may hide the symptom, but it does not fix the underlying problem.

---

## Common anti-patterns

Avoid:

- calling `time.sleep(...)`
- polling loops in test code
- try/except blocks to retry actions
- passing timeout values through test helpers

All of these duplicate framework behavior and reduce stability.

---

## Key takeaways

- Waiting is implicit and framework-managed
- Timeouts come from global configuration
- Tests express intent, not timing
- Page Objects and widgets encode readiness
- Failures after timeout indicate real issues

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Writing Stable Tests](/docs/how-to/write-stable-tests.md)  
→ Next: [Handling Animations and Dynamic Content](/docs/how-to/handle-animations.md)
