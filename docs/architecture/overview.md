← [Back to Documentation Index](/docs/index.md)  
← Previous: [Page Object Layout Patterns](/docs/examples/patterns/page-object-layouts.md)  
→ Next: [Execution Model](/docs/architecture/execution-model.md)

---
# 8.1 High-Level Architecture Overview

Hyperion is designed as a **structural automation framework**, not a command-driven one.

Instead of treating automation as a linear sequence of imperative commands executed against a backend, Hyperion models the system under test as a **stable, hierarchical object graph** and resolves execution concerns dynamically at runtime.

This architectural choice is the foundation for:

- cross-platform reuse  
- automatic context switching  
- error resilience and recovery  
- deterministic, hierarchical logging  
- stable Page Object and Widget composition  

This chapter explains **how Hyperion is structured internally** and **why it behaves the way it does at runtime**.

---

## Architectural goals

Hyperion’s architecture is guided by a small set of explicit goals.

### Separate structure from execution

Hyperion draws a strict boundary between:

- **Structure** — what the system *is*  
  (pages, widgets, elements, context boundaries)
- **Execution** — how interactions are *performed*  
  (drivers, protocols, retries, waits, context switching)

Page Objects describe structure and behavior.  
Execution is resolved later, at the moment of interaction.

This separation allows the same Page Object Model to operate across:
- web, mobile, desktop, and hybrid UIs
- different automation backends
- different execution environments

---

### Favor composition over control flow

Hyperion does not expect users to manage:

- context switches
- retries
- stale element recovery
- synchronization timing
- backend-specific commands

Instead, these concerns are **composed into the framework** and applied automatically based on the object hierarchy.

User code expresses *intent*.  
The framework determines *how* that intent is executed.

---

### Treat UI as a hierarchy, not a flat surface

Modern applications are hierarchical by nature:
- pages contain sections
- sections contain components
- components contain elements
- some components introduce context boundaries (iframes, webviews, windows)

Hyperion models this explicitly.

The Page Object Model is treated as a **virtual UI tree** whose structure mirrors the real application, even though the underlying UI may be re-rendered, replaced, or recreated at runtime.

---

## High-level system layers

At a conceptual level, Hyperion is composed of four cooperating layers.

### 1. Test layer

The test layer is responsible only for:
- expressing intent
- providing input data
- asserting outcomes

Tests do **not**:
- manage execution context
- perform synchronization
- handle retries or recovery
- interact with backend APIs directly

This keeps tests short, readable, and stable.

---

### 2. Page Object Model (POM) layer

The Page Object Model is the **structural core** of Hyperion.

It defines:
- pages, widgets, and elements
- hierarchy and containment
- behavior expressed as methods
- logical context boundaries (iframes, webviews, windows)

Page Objects and Widgets:
- are static Python objects
- can be safely cached and reused
- act as stable handles to dynamic UI state

This layer behaves like a **virtual DOM**:
- detached from any specific backend
- persistent across UI mutations
- capable of re-resolving execution details on demand

---

### 3. Execution and resolution layer

This layer is responsible for turning *structure* into *action*.

It handles:
- locator resolution (platform / OS / viewport)
- element lookup relative to parent scope
- automatic context switching
- waits, retries, and stale recovery
- timeout and policy enforcement

Execution is **lazy**:
- nothing is resolved until an interaction or assertion occurs
- resolution always happens in the correct structural context

Failures at this layer are treated as **automation instability**, not test failure, and are handled through bounded recovery mechanisms.

---

### 4. Backend abstraction layer

The backend abstraction layer adapts Hyperion’s execution model to concrete technologies, such as:
- UI automation backends
- REST clients
- CLI / SSH sessions
- visual comparison engines

This layer:
- normalizes backend behavior behind a consistent API
- does not invent or reinterpret backend capabilities
- allows multiple backends to coexist under the same structural model

Backends are interchangeable **execution providers**, not architectural drivers.

---

## Static structure, dynamic execution

One of Hyperion’s core architectural principles is:

> **Structure is static. Execution is dynamic.**

Page Objects, Widgets, and Elements:
- are created once
- retain their identity
- preserve parent–child relationships

Execution details:
- element handles
- driver references
- context selections
- backend objects

are **replaceable and transient**.

When the UI changes:
- structure remains valid
- execution details are re-resolved
- interactions continue without leaking instability into user code

This principle underpins:
- safe caching of Page Objects
- automatic stale recovery
- correct context restoration

---

## Architecture as an enabler, not a constraint

Hyperion’s architecture is intentionally opinionated.

It restricts certain patterns:
- manual context switching
- backend-specific logic in tests
- ad-hoc synchronization
- flat, locator-only Page Objects

In return, it enables:
- expressive, intention-driven tests
- deep UI composition
- cross-platform reuse
- predictable, readable execution logs

The remaining chapters in this section build on this overview by describing **how each subsystem fulfills its role within this architecture**.
---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Page Object Layout Patterns](/docs/examples/patterns/page-object-layouts.md)  
→ Next: [Execution Model](/docs/architecture/execution-model.md)
