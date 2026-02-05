← [Back to Documentation Index](/docs/index.md)  
← Previous: [Automatic Context Switching](/docs/core-concepts/context-switching.md)  
→ Next: [Your First Web Test](/docs/tutorials/first-web-test.md)

---

# Stale Element Recovery and Retries

UI automation does not fail only because systems are broken.
Very often, it fails because **the UI is changing while it is being observed**.

Modern applications continuously mutate:
- DOM nodes are replaced
- components are re-rendered
- contexts are recreated
- lists are rebuilt asynchronously

These changes frequently surface as *stale* or *context-related* errors.
Hyperion treats such errors as **transient automation failures**, not as test failures.

This chapter explains **how Hyperion provides error resilience**, what it recovers from,
and where recovery intentionally stops.

---

## Why transient automation errors exist

Automation interacts with a **moving target**.

Between locating an element and interacting with it, the UI may:
- re-render a component
- update part of the DOM tree
- recreate an iframe or embedded view
- change execution context

In these situations, the previously valid reference becomes outdated.
This does not necessarily mean:
- the UI is broken
- the test logic is wrong
- the user flow is invalid

It simply means the snapshot of the UI has changed.

Hyperion is designed to absorb this kind of instability.

---

## What “stale” really represents

A *stale* reference is not a broken element.
It is a **reference to a UI node that no longer exists in its previous form**.

Conceptually:
- the UI moved on
- the reference did not

Stale errors are therefore signals of **desynchronization**, not incorrect intent.
They indicate that recovery may be possible if the UI structure is re-evaluated.

---

## Error resilience vs test correctness

Hyperion’s recovery mechanisms are explicitly **not** about fixing test failures.

They do **not**:
- change verification outcomes
- retry failed assertions
- correct incorrect expectations
- hide real product bugs

Instead, Hyperion focuses on **resilience to common automation errors**, such as:
- stale references
- transient context invalidation
- short-lived structural inconsistencies

Verification failures remain verification failures.
Recovery applies only to **interaction and resolution**, not correctness.

---

## Recovery is hierarchy-aware

Recovery in Hyperion is **structure-aware**, not element-centric.

Although an error typically surfaces on a target element, the root cause may lie:
- in the element itself
- in its parent widget
- in an ancestor context
- or higher in the UI structure

For this reason, Hyperion never re-resolves elements blindly from the document root.

Instead:
- locators are always applied **relative to their modeled parent**
- recovery respects the Page Object hierarchy
- parent–child relationships are preserved

If recovery at one level fails, Hyperion moves **up the structure**, reapplying
each locator in sequence until stability is restored or the document boundary is reached.

This ensures that **tree integrity is preserved**, even after re-renders or context recreation.

---

## Recovery is iterative and bounded

UI mutation may still be happening **while recovery itself is in progress**.

A single recovery attempt is often insufficient:
- the DOM may continue changing
- a different node may become stale
- a parent context may be recreated

For this reason, recovery is:
- **iterative** — allowing the UI time to stabilize
- **bounded** — never infinite
- **scoped** — limited to the modeled structure

Retries exist to defend against *ongoing mutation*, not to “try until it works”.

Hyperion gives the UI a **bounded stabilization window**, then makes a clear decision.

---

## When recovery stops and failures become real

If recovery cannot restore a valid structure within its bounds, the failure changes in nature.

Instead of repeated stale or context errors, the system eventually reports that:
- the element no longer exists
- the structure cannot be resolved
- the modeled UI is no longer present

This transition is intentional.

It ensures that:
- transient instability is absorbed
- real structural changes surface clearly
- failures become more meaningful over time

Recovery does not hide problems — it **filters noise** until only real issues remain.

---

## Designing page objects for resilient recovery

Well-designed Page Object Models make recovery more effective.

Conceptual guidelines:
- model repeated structures as collections
- avoid caching UI state outside the model
- keep locators scoped to their logical parents
- express synchronization at semantic boundaries
- let structure, not test logic, drive resolution

When the POM accurately reflects UI structure, Hyperion can recover confidently
without guessing or overreaching.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Automatic Context Switching](/docs/core-concepts/context-switching.md)  
→ Next: [Your First Web Test](/docs/tutorials/first-web-test.md)