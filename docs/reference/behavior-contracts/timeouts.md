← [Back to Documentation Index](/docs/index.md)  
← Previous: [Context Switching Rules](/docs/reference/behavior-contracts/context-switching.md)  
→ Next: [Logging Behavior](/docs/reference/behavior-contracts/logging.md)

---

# 6.3 Retry and Timeout Semantics

This page defines **guarantees** for retries, timeouts, and stale-element recovery.

Hyperion’s stability model assumes that many UI failures are not “test failures”, but transient conditions such as:

- DOM mutations
- stale references
- delayed rendering
- temporary unavailability during UI updates

Hyperion retries these conditions automatically to maximize test stability.

---

## Defaults and configuration

Timeouts and retry parameters are configuration-driven.

Default values (as shipped):

### PageObject config
```python
class PageObject(Section):
    def __init__(self):
        self.start_retries = 3
        self.retry_delay = 1
```

### Element config
```python
class Element(Section):
    def __init__(self):
        self.search_attempts = 3
        self.search_retry_timeout = 0.5
        self.stale_recovery_timeout = 0.5
        self.wait_timeout = 30
        self.missing_timeout = 5
```

Guarantee:

- These values are configurable via Hyperion configuration.
- Contract semantics remain the same regardless of tuning.

---

## Retry model: 3 retries per node, exponential with depth

Guarantee:

- Hyperion performs **3 retries per node** during resolution and interaction.
- Because resolution walks the Page Object hierarchy, the total retry work can grow **exponentially with node depth**.

This time cost is intentional: it is the mechanism that allows Hyperion to recover from transient UI instability and raise exceptions only on real failures.

---

## Stale element recovery is scope-preserving

Guarantee:

- On stale-related failures, Hyperion can re-resolve the element from its **parent scope**, not from the global document/root.
- Because parent scope is known in the Page Object “virtual DOM” hierarchy, recovery preserves correct context and scope.

This enables:

- safe refresh of internal element references
- correct behavior across iframes/webviews
- recovery without requiring test code to restart flows

---

## Timeouts: interactive waiting, not passive sleeping

Guarantee:

- Hyperion timeouts are used to repeatedly attempt progress under observable conditions.
- Hyperion does not rely on passive sleeps as part of the stability model.

(Individual projects may add sleeps for demo pacing, but the stability model is built on retries + waits.)

---

## Relationship between retries and timeouts

Guarantee:

- Retries and timeouts work together to provide stability.
- When conditions remain unstable beyond configured limits, Hyperion raises an exception.

If you need to reason about test duration, consider both:

- per-attempt retry parameters (`search_attempts`, retry delays/timeouts)
- overall waits (`wait_timeout`, `missing_timeout`)

---

## Related documentation

- Context switching guarantees: `/docs/reference/behavior-contracts/context-switching.md`
- Locator resolution order: `/docs/reference/behavior-contracts/locator-resolution.md`
- Writing stable tests (how-to): `/docs/how-to/write-stable-tests.md`

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Context Switching Rules](/docs/reference/behavior-contracts/context-switching.md)  
→ Next: [Logging Behavior](/docs/reference/behavior-contracts/logging.md)
