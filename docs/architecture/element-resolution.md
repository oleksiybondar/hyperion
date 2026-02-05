← [Back to Documentation Index](/docs/index.md)  
← Previous: [Page Object Lifecycle](/docs/architecture/page-object-lifecycle.md)  
→ Next: [Waits, Retries, and Synchronization](/docs/architecture/waits-and-retries.md)

---

# 8.4 Element Resolution and Caching

Element resolution in Hyperion is **structural, scoped, and repeatable**.

Unlike traditional automation frameworks that resolve elements eagerly and cache backend handles, Hyperion treats elements as **logical references** that are resolved on demand, relative to their position in the Page Object hierarchy.

This chapter explains how element resolution works, how caching is applied safely, and why this approach remains stable even when the UI is not.

---

## Elements are resolved, not stored

In Hyperion, an `Element` object does not store:
- a DOM node
- an accessibility object
- a backend-specific element handle

Instead, it stores:
- a locator declaration
- a reference to its parent structural object
- metadata required for resolution and logging

When an interaction or assertion occurs, the element is **resolved**, used, and then released or replaced as needed.

This distinction is fundamental:
> Hyperion caches **structure**, not **execution artifacts**.

---

## Parent-scoped resolution

Element resolution is always **relative to the parent scope**.

Resolution never starts from the global document or application root unless the element itself is defined at that level.

The resolution process proceeds as follows:

1. Resolve the parent scope (page, widget, iframe, webview)
2. Apply the parent’s locator within its own scope
3. Continue downward through the hierarchy
4. Resolve the target element within the final scoped context

This ensures that:
- identical locators in different parts of the UI do not conflict
- nested components remain isolated
- recovery can re-walk the hierarchy safely

---

## Locator resolution before element lookup

Before any backend lookup occurs, the element’s locator declaration is resolved into a concrete selector.

Locator resolution may consider:
- platform (web, mobile, desktop)
- operating system (e.g. Android, iOS, Windows, macOS)
- viewport or layout breakpoint (when explicitly declared)

Resolution is:
- explicit
- deterministic
- recursive

If a locator does not declare variation, it is treated as static and no resolution logic is applied.

---

## Resolution is recursive and hierarchical

Locator resolution does not depend on how locator mappings are nested in code.

At runtime:
- all declared variations are evaluated
- incompatible branches are excluded
- the most specific applicable locator is selected

This recursive approach ensures that:
- nesting order is a modeling choice, not an execution constraint
- resolution remains consistent across complex declarations
- unsupported environments fail explicitly rather than guessing

---

## Element caching semantics

Hyperion may cache **resolved execution state** temporarily, but this cache is always:
- scoped to the element
- bound to the current context
- invalidated on failure

Caching exists to:
- avoid unnecessary backend lookups
- reduce execution overhead
- improve performance in stable UI regions

It does **not** imply long-lived backend handles.

If a cached reference becomes invalid:
- a stale or context error is raised
- recovery logic is triggered
- the element is re-resolved from its parent scope

---

## Caching and UI mutation

UI mutation is expected.

When the UI changes:
- cached backend references may become stale
- structural objects remain valid
- resolution is re-attempted transparently

Because resolution always starts from the parent scope, Hyperion can:
- reapply locators safely
- rebuild execution state
- preserve correct context boundaries

This makes element caching compatible with:
- re-rendered components
- replaced DOM subtrees
- recreated iframes or webviews

---

## Why global caching is avoided

Hyperion intentionally avoids:
- global element caches
- document-level lookups by default
- long-lived backend references

These patterns are fragile in dynamic applications and make recovery unreliable.

By scoping resolution and caching to the hierarchy, Hyperion ensures that:
- failures are localized
- recovery is predictable
- execution remains explainable

---

## Element identity vs element existence

An important architectural distinction:

- **Element identity** is structural and persistent  
- **Element existence** is runtime-dependent and transient

An element object may exist even when:
- the UI has not yet rendered
- the element is temporarily missing
- the context is not currently active

Existence is checked during resolution and interaction, not at declaration time.

---

## Summary

Element resolution in Hyperion is:

- lazy
- parent-scoped
- hierarchy-aware
- context-sensitive
- resilient to UI mutation

Caching is applied carefully to execution state, never to structure.

This model allows Hyperion to remain stable and predictable in environments where the UI itself is anything but.

The next chapter builds on this foundation by explaining how waits, retries, and synchronization are applied during resolution and interaction.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Page Object Lifecycle](/docs/architecture/page-object-lifecycle.md)  
→ Next: [Waits, Retries, and Synchronization](/docs/architecture/waits-and-retries.md)