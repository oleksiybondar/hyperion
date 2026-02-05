← [Back to Documentation Index](/docs/index.md)  
← Previous: [Locator Resolution Model](/docs/core-concepts/locator-resolution.md)  
→ Next: [Stale Element Recovery and Retries](/docs/core-concepts/retry-and-recovery.md)

---

# Automatic Context Switching

Modern applications are rarely flat.

They embed content from multiple sources, open new execution surfaces, and mix
technologies that require different execution contexts.

Hyperion is designed so that **tests do not need to manage these context changes explicitly**.
Instead, context switching is modeled as part of the UI structure and handled automatically
by the framework.

This chapter explains **why context switching exists**, **how it fits into the Page Object Model**,
and **what guarantees Hyperion provides**.

---

## Why context switching exists

Context switching is required whenever interacting with part of the system requires
changing the execution environment.

Common examples include:
- web pages embedding content in iframes
- mobile applications embedding webviews
- actions that open new windows or tabs
- applications that mix native and embedded browser surfaces
- tools that expose multiple logical execution scopes

From a user’s perspective, these are still part of a **single flow**.
From an automation perspective, they often require switching context before interaction.

Hyperion’s goal is to prevent this mismatch from leaking into test code.

---

## Contexts as part of the UI structure

In Hyperion, a context boundary is treated as a **structural element of the UI**, not a
procedural concern.

If part of the UI requires a different execution context:
- it appears explicitly in the Page Object Model
- it occupies a position in the object hierarchy
- it can contain elements and widgets like any other node

This means that:
- iframes
- webviews
- windows
- embedded execution surfaces

are modeled the same way as other structural components.

The Page Object Model does not flatten context boundaries — it **represents them**.

---

## Automatic switching and scope

“Automatic” context switching does not mean implicit or unpredictable.

It means that:
- switching occurs when entering a modeled context node
- interactions within that node run in the correct execution scope
- the previous scope is restored when leaving that node

From the test’s point of view:
- no explicit switching calls are required
- interactions appear linear and readable
- the model determines the active context

Context switching is therefore:
- deterministic
- structural
- driven by object access, not by individual actions

---

## Nested contexts

Context boundaries can be nested.

Examples include:
- an iframe inside another iframe
- a webview embedded inside a mobile screen
- a dialog opened inside a secondary window

Hyperion treats nested contexts the same way it treats nested widgets:
- the object hierarchy reflects the UI hierarchy
- deeper access paths represent deeper context scopes
- switching follows the modeled structure

This allows complex UI compositions to be represented without special handling
in test code.

Nested contexts are not an edge case — they are a natural consequence of modern UI design.

---

## What automatic switching guarantees (and what it doesn’t)

Automatic context switching provides strong guarantees, but it is not magic.

### What Hyperion guarantees

- The correct execution context is active when interacting with modeled elements
- Context boundaries are respected according to the object hierarchy
- Context is restored when leaving a scoped interaction
- Tests do not need to manage context explicitly

These guarantees allow test code to remain clean and intention-focused.

---

### What Hyperion does *not* guarantee

- It does not make broken or unreachable UI work
- It does not hide synchronization problems
- It does not replace waiting or retry mechanisms
- It does not guess or recover from incorrectly modeled structure

Context switching ensures **correct scope**, not **correct timing** or **correct state**.

---

## Why automatic context switching belongs in the POM

Keeping context switching inside the Page Object Model ensures that:
- execution complexity stays out of tests
- UI structure remains explicit
- one logical model can span multiple execution environments

Tests can focus on:
> “What is the user doing?”

instead of:
> “Which context am I in right now?”

That separation is essential for readable, maintainable automation at scale.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Locator Resolution Model](/docs/core-concepts/locator-resolution.md)  
→ Next: [Stale Element Recovery and Retries](/docs/core-concepts/retry-and-recovery.md)
