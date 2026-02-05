← [Back to Documentation Index](/docs/index.md)  
← Previous: [Element Resolution and Caching](/docs/architecture/element-resolution.md)  
→ Next: [Context Switching Internals](/docs/architecture/context-switching.md)

---

# 8.5 Waits, Retries, and Synchronization

Hyperion treats synchronization as an **execution stability problem**, not a test logic concern.

Modern applications are highly dynamic:
- DOM nodes are replaced
- components are re-rendered
- contexts are recreated
- UI state changes asynchronously

Hyperion’s architecture assumes this instability is normal and designs synchronization mechanisms to **absorb transient execution failures** while preserving strict test correctness.

---

## Stability vs correctness

A fundamental architectural distinction in Hyperion is the separation between:

- **Execution stability**  
  Can the framework reliably perform the requested interaction?

- **Test correctness**  
  Does the system under test behave as expected?

Waits, retries, and recovery apply **only** to execution stability.

Assertions, expectations, and verifications are **never softened** by retries intended to stabilize execution.

This ensures that:
- flaky execution does not cause false failures
- real product defects are not masked

---

## Implicit synchronization

Hyperion does not require users to write explicit waits in tests.

Synchronization is applied:
- automatically
- implicitly
- at the point of interaction or assertion

Examples of implicitly synchronized operations include:
- clicking an element
- reading text or attributes
- checking visibility or presence
- performing assertions

The framework waits for observable conditions relevant to the operation being performed, rather than relying on fixed delays.

---

## Retry model overview

Hyperion applies a **bounded retry model** to execution operations.

Key characteristics:

- retries are finite
- retries are applied per structural node
- retries increase with hierarchy depth
- retries are transparent to user code

The default retry policy allows **multiple attempts per node**, which results in an **exponential retry window** relative to the depth of the Page Object hierarchy.

This is intentional.

---

## Why retries scale with hierarchy depth

Failures in deeper structures are more likely to be caused by:

- parent re-rendering
- container replacement
- iframe or webview recreation
- cascading UI updates

By allowing more recovery attempts at deeper levels, Hyperion gives the UI sufficient time to stabilize **without guessing** or blocking indefinitely.

Shallow failures recover quickly.  
Deep failures are given more opportunity to resolve.

If stability cannot be achieved within the allowed window, the failure is escalated.

---

## Recovery-driven retries

Retries in Hyperion are not simple re-executions of the same command.

When an execution error occurs (for example, a stale or context-related failure):

1. The current execution attempt is aborted
2. Cached execution state is invalidated
3. Resolution restarts from the failing node
4. Parent scopes may be re-resolved
5. Context selection may be revalidated or forced

This **recovery-first approach** ensures that retries adapt to the current UI state rather than repeating invalid assumptions.

---

## What is considered recoverable

Hyperion treats the following as recoverable execution failures:

- stale element references
- transient context invalidation
- short-lived absence of UI elements
- temporary backend inconsistencies

These errors indicate that the UI has changed, not that the test intent is wrong.

---

## What is not recoverable

The following are **not** retried by the framework:

- failed assertions or expectations
- verification mismatches
- explicitly raised test errors
- invalid locator declarations
- structural mismatches in the Page Object Model

These failures represent **logical or correctness issues** and must surface immediately.

---

## Timeouts as policy

Timeouts in Hyperion are:
- configurable
- centralized
- treated as execution policy

Timeout values define:
- how long the framework is allowed to wait
- how long recovery may continue
- when a failure becomes final

Timeouts do not change behavior — they bound it.

This allows teams to tune execution tolerance without altering test logic.

---

## No sleeps, no polling loops

Hyperion intentionally discourages:
- `sleep()` calls
- manual polling loops
- timing assumptions in Page Objects or tests

These patterns:
- reduce determinism
- hide real synchronization issues
- break across environments

Instead, Hyperion synchronizes on **observable UI state** and retries resolution when that state is in flux.

---

## Synchronization as a framework concern

A core architectural rule:

> Tests and Page Objects must not manage synchronization explicitly.

User code should not:
- retry operations
- wait for backend-specific signals
- guess when the UI is “ready”

The framework owns synchronization so that:
- test intent remains clear
- behavior remains consistent
- execution remains debuggable

---

## Summary

Hyperion’s synchronization model is:

- implicit
- recovery-driven
- hierarchy-aware
- bounded
- policy-controlled

By treating instability as an execution concern and correctness as a test concern, Hyperion achieves stability without sacrificing truth.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Element Resolution and Caching](/docs/architecture/element-resolution.md)  
→ Next: [Context Switching Internals](/docs/architecture/context-switching.md)
