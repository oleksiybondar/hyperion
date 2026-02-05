← [Back to Documentation Index](/docs/index.md)  
← Previous: [Execution Model](/docs/architecture/execution-model.md)  
→ Next: [Element Resolution and Caching](/docs/architecture/element-resolution.md)

---

# 8.3 Page Object Lifecycle

Hyperion’s Page Object Model is designed around **long-lived structural objects** and **short-lived execution state**.

Understanding the lifecycle of Page Objects, Widgets, and Elements is essential for understanding why:
- object caching is safe
- references remain valid across UI mutations
- recovery and re-resolution work reliably
- context switching does not leak between interactions

This chapter explains how Page Objects live, how they change, and what never changes.

---

## Static objects, dynamic state

In Hyperion, Page Objects, Widgets, and Elements are:

- created once per logical UI surface
- represented as regular Python objects
- organized into a persistent parent–child hierarchy

These objects **do not represent a snapshot of the UI**.

Instead, they represent a **structural contract**:
- what exists
- how it is composed
- how it can be interacted with

By contrast, execution state — such as backend element handles, driver references, or selected contexts — is **transient** and may change many times during the lifetime of the same Page Object.

---

## Instantiation and decoration

Page Objects and Widgets are instantiated when:
- a page is opened
- a screen or application is launched
- a widget is first accessed as part of a hierarchy

At instantiation time, Hyperion applies:
- decorators for elements, widgets, iframes, and webviews
- logging wrappers around user-defined methods
- structural metadata used for resolution and logging

This happens **once**, not on every interaction.

The result is a stable object graph whose behavior does not change even if the underlying UI does.

---

## Elements as resolvable handles

An `Element` in Hyperion is not a DOM node, accessibility object, or backend handle.

It is a **resolvable handle** that contains:
- a locator declaration
- a reference to its parent scope
- structural metadata

When an interaction occurs:
- the element is resolved relative to its parent
- a backend handle is obtained or refreshed
- the action is performed
- the handle may be discarded or replaced later

The Python object representing the element remains the same throughout this process.

---

## Lifecycle across UI mutation

Modern UIs frequently:
- re-render components
- replace DOM subtrees
- recreate iframes or webviews
- destroy and rebuild views

Hyperion assumes this is normal.

When UI mutation occurs:
- existing backend references may become invalid
- structural objects remain valid
- resolution is repeated on demand

This allows Page Objects and Widgets to survive:
- DOM replacement
- navigation within the same page
- context recreation
- transient backend failures

The lifecycle of structural objects is therefore **independent of UI stability**.

---

## Parent–child integrity

Each Page Object, Widget, and Element:
- knows its parent
- preserves its position in the hierarchy
- never loses structural context

This parent–child chain is the backbone of:
- scoped element resolution
- correct context selection
- hierarchical recovery
- meaningful logging

Even when execution state is reset or replaced, the structural chain remains intact.

---

## Safe caching and reuse

Because structure and execution are separated, it is safe to:

- cache Page Objects
- store Widget references
- pass Elements between methods
- reuse iframe and webview objects

Caching does **not** imply caching backend handles.

Instead, it preserves:
- structure
- intent
- hierarchy

Backend state is always resolved dynamically when needed.

---

## Method calls and behavioral stability

User-defined methods on Page Objects and Widgets:
- are decorated once at instantiation time
- are logged consistently across calls
- do not depend on backend state

This ensures that:
- repeated method calls behave identically
- logs remain readable and hierarchical
- failures can be traced to intent-level operations

Behavior is stable even when execution details change.

---

## Lifecycle boundaries

A Page Object’s lifecycle typically ends when:
- the test case ends
- the execution context is explicitly closed
- the underlying application is terminated

Until then, the Page Object and its children remain valid structural references.

Destroying and recreating Page Objects manually is rarely necessary and usually indicates a modeling issue.

---

## Summary

The Page Object lifecycle in Hyperion is defined by a clear separation:

- **Structure** lives for the duration of the test flow
- **Execution state** is resolved, replaced, and recovered as needed

By treating Page Objects as a virtual, persistent representation of the UI, Hyperion enables:
- resilient execution
- safe reuse
- deep composition
- predictable recovery

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Execution Model](/docs/architecture/execution-model.md)  
→ Next: [Element Resolution and Caching](/docs/architecture/element-resolution.md)
