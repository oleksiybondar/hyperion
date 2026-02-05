← [Back to Documentation Index](/docs/index.md)  
← Previous: [High-Level Architecture Overview](/docs/architecture/overview.md)  
→ Next: [Page Object Lifecycle](/docs/architecture/page-object-lifecycle.md)

---

# 8.2 Execution Model

Hyperion’s execution model is built around a single guiding idea:

> **Execution is resolved at the moment of interaction, not at declaration time.**

Page Objects, Widgets, and Elements declare *what exists* and *how it relates*.  
The execution model determines *how and when* those declarations are turned into real actions against a backend.

This separation allows Hyperion to remain stable in the presence of:
- dynamic UI mutation
- context recreation
- backend differences
- asynchronous rendering

---

## Lazy execution

Hyperion does not eagerly resolve elements, contexts, or backend handles.

No execution happens when:
- Page Objects are instantiated
- widgets are accessed
- elements are referenced as attributes

Execution begins only when:
- an interaction is requested (e.g. click, fill)
- a wait condition is evaluated
- an assertion or verification is performed

This **lazy execution** model ensures that:
- resolution always reflects the current UI state
- stale references are avoided whenever possible
- context switching decisions are made with up-to-date information

---

## Execution as a resolution pipeline

When an interaction is triggered, Hyperion executes a structured resolution pipeline.

At a high level, the pipeline consists of:

1. **Structural validation**  
   Confirm the element belongs to a valid Page Object hierarchy.

2. **Context resolution**  
   Determine the correct execution context based on:
   - parent containers
   - iframe or webview boundaries
   - previously selected context state

3. **Locator resolution**  
   Resolve the locator declaration into a concrete selector based on:
   - platform
   - operating system
   - viewport (if applicable)

4. **Element lookup**  
   Locate the element relative to its **parent scope**, never globally by default.

5. **Synchronization and waiting**  
   Apply implicit waits and readiness checks as defined by policy.

6. **Interaction or assertion execution**  
   Perform the requested action or validation against the backend.

Each step is deterministic and repeatable.

---

## Hierarchy-aware execution

Execution in Hyperion is always **hierarchy-aware**.

An element is never resolved in isolation:
- it is resolved relative to its parent widget or page
- parent locators are applied first
- child locators are applied incrementally

This guarantees that:
- execution scope is always correct
- nested components remain stable
- recovery can walk the hierarchy safely

This design mirrors how modern UI frameworks reason about component trees rather than flat DOM queries.

---

## Retry and recovery as part of execution

Transient automation failures are expected in modern applications.

Common causes include:
- DOM re-rendering
- element replacement
- context recreation
- asynchronous UI updates

Hyperion treats these as **execution instability**, not test failure.

During execution:
- each node in the hierarchy is retried a bounded number of times
- retry depth increases with structural depth
- recovery proceeds from the failing node upward

This results in an **exponential retry window** relative to hierarchy depth, which is intentional:
- shallow failures recover quickly
- deeper failures allow more stabilization time

If recovery succeeds, execution continues transparently.  
If recovery is exhausted, the failure is escalated as a real error.

---

## Context-aware execution

Execution is always bound to a specific context:
- document context
- iframe context
- webview or native context
- window or application context

Context selection is:
- automatic
- state-aware
- validated before execution

Hyperion tracks the currently selected context and compares it against the required context for each interaction.

Context switching occurs only when necessary and is restored automatically after execution completes.

This ensures:
- minimal backend switching
- predictable execution flow
- no context leakage across interactions

---

## Execution vs correctness

Hyperion makes a strict distinction between:

- **Execution correctness**  
  Did the framework successfully perform the interaction?

- **Test correctness**  
  Did the system under test behave as expected?

Retries, recovery, and synchronization apply **only** to execution correctness.

Assertions and expectations:
- are never retried implicitly
- fail immediately when violated
- represent test-level truth

This separation prevents recovery mechanisms from masking real product defects.

---

## Execution as a framework responsibility

A core architectural principle of Hyperion is that:

> Tests should never orchestrate execution mechanics.

User code does not:
- wait explicitly
- retry manually
- switch context
- handle stale references
- interact with backend APIs

Instead, tests describe intent and verify outcomes.  
The execution model ensures that intent is carried out reliably.

---

## Deterministic execution and logging

Every execution step is:
- observable
- logged
- associated with a structural path

This produces logs that:
- reflect the Page Object hierarchy
- show retries and recovery explicitly
- explain context switches and decisions

Execution transparency is a first-class requirement, not a debugging aid.

---

## Summary

Hyperion’s execution model is:
- lazy
- hierarchy-aware
- context-aware
- recovery-driven
- backend-agnostic

By resolving execution at the moment it is needed and grounding it in structure, Hyperion achieves stability without sacrificing clarity or control.

Subsequent chapters explore the internal mechanics of these execution stages in more detail.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [High-Level Architecture Overview](/docs/architecture/overview.md)  
→ Next: [Page Object Lifecycle](/docs/architecture/page-object-lifecycle.md)
