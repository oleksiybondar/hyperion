← [Back to Documentation Index](/docs/index.md)  
← Previous: [Element vs Elements (singular vs plural)](/docs/core-concepts/element-vs-elements.md)  
→ Next: [Automatic Context Switching](/docs/core-concepts/context-switching.md)

---

# Locator Resolution Model

In Hyperion, a locator is not just a selector string — it is a **declaration of intent**.

Most of the time, that declaration is simple and static.  
In more complex systems, the same intent may need to be fulfilled differently depending on
platform, operating system, or layout.

This chapter explains **how Hyperion thinks about locator resolution**, and why it exists,
without going into API or implementation details.

---

## Locators as declarations, not selectors

A locator describes **what UI element is being targeted**, not every possible way to find it.

In many projects, a locator maps directly to a single selector and never varies.
In these cases, Hyperion behaves exactly like a traditional framework:
- the locator is static
- no contextual resolution is involved
- no additional logic is applied

The locator resolution model exists to handle the cases where **reality diverges**, not to
complicate the common path.

---

## Static locators are the default

Static locators are the normal and expected case.

If a locator does **not** define any variation:
- it is treated as static
- resolution logic is never invoked
- the locator behaves as a single, fixed selector

In other words:

> If no variation is declared, nothing dynamic happens.

This makes locator resolution **explicit and opt-in**, rather than implicit or magical.

---

## Why locators sometimes need to vary

Modern systems often share the same **user flow** while differing in **UI structure**.

Common reasons include:
- responsive design with different layouts at different viewport sizes
- separate technology stacks for mobile and desktop
- fundamentally different locator strategies for web, mobile, and desktop automation

In these cases:
- the *intent* stays the same
- the *structure* changes

Locator resolution exists to preserve **one logical Page Object Model** across these variations,
so that tests remain reusable and intention-focused.

The goal is not to make locators dynamic —  
the goal is to keep the model stable when the UI is not.

---

## Dimensions that influence resolution

When variation is explicitly declared, Hyperion may resolve a locator based on a small,
well-defined set of dimensions.

### Platform
The high-level execution domain:
- `web`
- `mobile`
- `desktop`

Platform is typically known from the execution environment and is inexpensive to resolve.

---

### Operating System
The operating system within a platform, such as:
- iOS
- Android
- Windows
- macOS

OS resolution is also capability-based and must be **explicitly defined** when used.

---

### Viewport
Viewport represents layout variation within the same UI surface.

Common labels include:
- `xs`, `sm`, `md`, `lg`, `xl`

Viewport resolution may require additional runtime inspection, such as:
- screen size
- page size
- orientation

For this reason, viewport is treated as a **layout concern**, not a platform concern.

Viewport breakpoints are configurable and, by default, follow Bootstrap-style conventions.

---

## Resolution is explicit and constrained

Locator resolution is intentionally **limited and deterministic**.

Key principles:
- Only known dimensions participate in resolution
- Unexpected or unknown keys are ignored
- No guessing or implicit fallback occurs

The structure used to declare variation is flexible:
- authors may group dimensions in the order that best reflects their domain
- nesting order is a modeling choice, not an execution contract

This allows clarity without sacrificing predictability.

---

## Viewport-specific fallback with `default`

Viewport variation supports a special fallback concept: **`default`**.

This reflects the reality of responsive design:
- most layouts are shared
- only specific breakpoints differ

Conceptually:
- `default` applies to all viewports unless explicitly overridden
- this fallback is **viewport-specific only**

For platform and operating system:
- all variations must be explicitly defined
- no implicit fallback is applied

This distinction prevents accidental cross-platform behavior while keeping responsive
models concise and expressive.

---

## Resolution priority at runtime

When multiple dimensions are involved, resolution follows a consistent conceptual priority:

1. Platform (if defined)
2. Operating system (if defined)
3. Viewport (if defined)

This priority reflects:
- how execution environments are determined
- the relative cost of resolving each dimension
- the fact that viewport is a refinement of an already-selected platform and OS

The exact mechanics of this process are covered in later sections of the documentation.

---

## Why locator resolution belongs in the POM

Keeping locator resolution inside the Page Object Model ensures that:
- tests remain declarative
- branching logic stays out of test code
- one logical model represents multiple realities

Instead of asking:
> “Which selector should I use here?”

Tests can ask:
> “What is the user interacting with?”

That separation is the core value of the locator resolution model.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Element vs Elements (singular vs plural)](/docs/core-concepts/element-vs-elements.md)  
→ Next: [Automatic Context Switching](/docs/core-concepts/context-switching.md)
