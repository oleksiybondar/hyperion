← [Back to Documentation Index](/docs/index.md)  
← Previous: [Context Switching Internals](/docs/architecture/context-switching.md)  
→ Next: [Backend Abstraction Layer](/docs/architecture/backend-abstraction.md)

---

# 8.7 Locator Resolution Internals

Locator resolution in Hyperion is designed to be **explicit, deterministic, and capability-driven**.

Rather than treating locators as static selectors or relying on conditional logic in tests, Hyperion allows Page Objects to declare **intent-level locator variation** and resolves the correct locator at runtime based on the active execution environment.

This chapter explains how locator resolution works internally and why it is structured the way it is.

---

## Locators as declarative intent

In Hyperion, a locator is a **declaration**, not an instruction.

A locator describes:
- what logical UI target is intended
- under which conditions different selectors apply

It does not describe:
- when to branch
- how to detect the environment
- which selector to try first procedurally

All decision-making happens inside the framework.

---

## Resolution dimensions

Locator resolution may consider a limited, well-defined set of dimensions:

1. **Platform**
   - web
   - mobile
   - desktop

2. **Operating system**
   - Android
   - iOS
   - Windows
   - macOS (Darwin)
   - Linux

3. **Viewport / layout breakpoint**
   - xs, sm, md, lg, xl (when explicitly declared)

These dimensions are derived from execution capabilities and runtime inspection, not from user code.

---

## Resolution priority

When multiple dimensions are involved, Hyperion applies a fixed conceptual priority:

1. Platform
2. Operating system
3. Viewport

This order reflects:
- how execution environments are established
- the relative cost of resolving each dimension
- the fact that viewport is a refinement within an already selected platform and OS

This priority is architectural, not configurable.

---

## Method of exclusion

Locator resolution in Hyperion uses a **method of exclusion**, not trial-and-error.

At runtime:
- all declared locator branches are evaluated
- branches incompatible with the current environment are excluded
- the most specific remaining branch is selected

There is no guessing and no sequential fallback.

If no compatible branch remains, resolution fails explicitly.

This guarantees:
- predictability
- debuggability
- early detection of unsupported environments

---

## Recursive resolution model

Locator declarations may be nested in any order that makes sense for the domain.

For example:
- platform → OS → viewport
- platform → viewport → OS
- viewport → platform (when appropriate)

The nesting structure is a **modeling choice**, not an execution constraint.

At runtime, Hyperion:
- walks the declaration recursively
- evaluates all dimensions independently
- applies exclusion rules consistently

This ensures that logical intent is preserved regardless of how the declaration is written.

---

## Viewport-specific fallback rules

Viewport resolution supports a special key: `default`.

- `default` applies to all viewports unless overridden
- specific viewport labels override `default`

This fallback exists **only for viewport variation**.

For platform and operating system:
- all supported branches must be explicitly declared
- no implicit fallback is applied

This prevents accidental cross-platform behavior and keeps resolution strict.

---

## Static locators are the default

If a locator declaration does not define any variation:
- it is treated as static
- resolution logic is bypassed entirely
- the locator is used as-is

This keeps the common case fast and simple.

Dynamic resolution is opt-in, not mandatory.

---

## Resolution vs element lookup

Locator resolution always occurs **before** element lookup.

The process is:

1. Resolve the locator declaration into a concrete selector
2. Resolve the execution context
3. Perform element lookup relative to the parent scope

This separation ensures that:
- resolution decisions are independent of UI state
- lookup failures are not conflated with resolution errors
- logs can explain *what was selected* separately from *what was found*

---

## Failure semantics

Locator resolution failures are treated as **structural errors**, not execution instability.

They indicate that:
- the Page Object does not support the current environment
- a required locator branch is missing
- the model no longer matches reality

Such failures are not retried.

They must be fixed by updating the Page Object model.

---

## Summary

Hyperion’s locator resolution model is:

- declarative
- capability-driven
- deterministic
- recursive
- strict by default

By resolving locator intent independently of execution flow, Hyperion enables:
- cross-platform reuse
- clean Page Object contracts
- predictable failure modes

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Context Switching Internals](/docs/architecture/context-switching.md)  
→ Next: [Backend Abstraction Layer](/docs/architecture/backend-abstraction.md)
