← [Back to Documentation Index](/docs/index.md)  
← Previous: [Waits, Retries, and Synchronization](/docs/architecture/waits-and-retries.md)  
→ Next: [Locator Resolution Internals](/docs/architecture/locator-resolution.md)

---

# 8.6 Context Switching Internals

Context switching is one of the most error-prone aspects of automation.

In many frameworks, it is exposed directly to users, forcing tests to:
- track the current context manually
- switch explicitly between frames or execution modes
- recover from invalid or stale context state

Hyperion takes a different architectural approach.

Context switching is treated as a **structural concern**, not a procedural one, and is handled entirely by the framework.

---

## Context as structural state

In Hyperion, a context represents an **execution boundary**, such as:
- a document boundary (iframe)
- an application-level boundary (webview)
- a window or application boundary
- a native vs web execution surface

Context boundaries are modeled explicitly in the Page Object hierarchy.

This means:
- contexts are declared structurally
- context transitions follow object access paths
- tests never “enter” or “exit” contexts manually

---

## Centralized context management

Hyperion maintains a dedicated internal manager responsible for:
- tracking the currently active execution context
- storing previously selected contexts
- validating whether a context switch is required
- restoring context after execution completes

This manager acts as the **single source of truth** for context state.

User code never manipulates this state directly.

---

## Context resolution at execution time

Context switching is evaluated **lazily**, at the moment an interaction or assertion occurs.

When execution begins, Hyperion:
1. Determines the required context based on the element’s position in the hierarchy
2. Compares it to the currently active context
3. Performs a switch only if the contexts differ
4. Records the previous context for later restoration

If the required context is already active, no switch occurs.

This avoids unnecessary backend operations and keeps execution efficient.

---

## Automatic context restoration

After an interaction completes, Hyperion:
- restores the previous context when appropriate
- preserves parent-level execution state
- prevents context leakage across interactions

This ensures that:
- sibling elements resolve correctly
- execution order does not matter
- nested context access remains safe

Context restoration is automatic and invisible to user code.

---

## Nested context boundaries

Context boundaries may be nested.

Common examples include:
- an iframe inside another iframe
- a webview containing multiple documents
- native application screens embedding web content

Hyperion handles nested contexts by:
- stacking context requirements
- resolving them in hierarchical order
- restoring them in reverse order

Nested context switching follows the same structural rules as nested widgets.

---

## Forced context resynchronization

Certain execution failures indicate that the stored context state may no longer reflect reality.

Examples include:
- stale context errors
- backend exceptions indicating invalid context
- unexpected context loss during execution

In these cases, Hyperion may:
- invalidate the stored context state
- force a context re-evaluation
- reselect the appropriate context from structure

This behavior is part of the recovery mechanism and ensures correctness even when background processes recreate execution surfaces.

---

## Manual context switching (discouraged)

Hyperion allows manual context switching in limited cases.

However, this is intentionally discouraged.

Manual switching:
- bypasses structural guarantees
- introduces hidden coupling between tests and execution mechanics
- makes recovery less predictable

The preferred approach is always to:
- model context boundaries structurally
- access elements through the Page Object hierarchy
- allow the framework to manage context transitions

Manual context control should be reserved for exceptional or experimental scenarios.

---

## Context switching and performance

Because context switching can be expensive, Hyperion optimizes for:
- minimal switches
- cached context identity
- comparison before switching

By switching only when necessary and restoring automatically, Hyperion achieves predictable performance even in complex nested scenarios.

---

## Summary

Hyperion’s context switching model is:

- structural, not procedural
- centralized and state-aware
- lazy and demand-driven
- recoverable and self-correcting
- invisible to user code

By embedding context boundaries directly into the Page Object Model, Hyperion eliminates an entire class of errors while preserving flexibility and performance.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Waits, Retries, and Synchronization](/docs/architecture/waits-and-retries.md)  
→ Next: [Locator Resolution Internals](/docs/architecture/locator-resolution.md)
