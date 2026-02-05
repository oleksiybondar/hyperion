← [Back to Documentation Index](/docs/index.md)  
← Previous: [Wait API and Timeouts](/docs/how-to/handle-waits-and-timeouts.md)  
→ Next: [Responsive (Viewport-Specific) Locators](/docs/how-to/responsive-locators.md)

---

# 4.3 Handling Animations and Dynamic Content

Modern applications are highly dynamic:

- components animate in and out
- layouts reflow
- DOM trees are re-rendered
- native UI elements are recreated
- content loads progressively

This guide explains **how Hyperion handles these conditions by design**, and how to write tests that remain stable without compensating logic.

---

## Animations are a source of transient states

Animations and dynamic updates often cause:

- elements to exist briefly, then disappear
- elements to be present but not yet interactable
- elements to be replaced with new instances
- layout shifts that temporarily invalidate locators

In many frameworks, these effects lead to flaky tests that require sleeps or retries.

In Hyperion, they are treated as **normal transient conditions**.

---

## Do not “wait for animations to finish”

A common anti-pattern is to explicitly wait for animations:

- waiting fixed time after click
- checking CSS animation properties
- polling for “animation complete” flags

These approaches are fragile because:

- animation timing varies across devices and environments
- animations may be skipped or shortened
- re-renders may replace elements mid-animation

Hyperion does **not** require tests to reason about animations explicitly.

---

## Why Hyperion tolerates animations naturally

Hyperion absorbs animation-related instability through a combination of guarantees:

- retries are automatic and bounded
- stale elements are re-resolved from parent scope
- resolution happens in the correct context
- failures occur only after recovery is exhausted

As a result:

- element replacement during animation is recoverable
- transient invisibility is tolerated
- re-rendered components do not break tests

From the test author’s perspective, animations “just happen”.

---

## Focus on semantic readiness, not visual completion

Instead of waiting for animations, tests and Page Objects should wait for **meaningful state**.

Examples of semantic readiness:

- result value is updated
- list contains expected items
- button becomes enabled
- status indicator reaches a final value
- count stops changing

Avoid:

- asserting intermediate visual states
- asserting that an animation is complete
- asserting pixel positions or transitions

Tests should assert **what the user ultimately cares about**, not how the UI gets there.

---

## Encode readiness in widgets and Page Objects

If a feature requires waiting for dynamic content to settle, encode that logic at the correct layer.

Good places:

- widget methods
- Page Object methods

Never in the test.

Conceptual example:

{codeblock}python
class NotificationPanel:
    def wait_until_stable(self):
        # wait until notifications stop changing
        ...
{codeblock}

The test simply calls `wait_until_stable()` as part of a higher-level action.

---

## Dynamic content and stale elements

Animations and re-renders often trigger stale element references.

Hyperion handles this by:

- re-resolving elements from their parent scope
- preserving correct context (iframe / webview / native)
- retrying interactions under bounded timeouts

Tests should **not** catch stale exceptions or retry actions manually.

If a stale error escapes the framework, it indicates a real issue.

---

## Avoid asserting intermediate states

Unstable tests often assert too early.

Avoid assertions like:

- “element is visible immediately after click”
- “count increments exactly once per animation frame”
- “DOM structure matches transitional layout”

Prefer assertions on **final state**:

- final value
- final count
- final status
- final UI condition

This keeps tests resilient to UI implementation changes.

---

## Animations across platforms

Different platforms behave differently:

- web animations vs CSS transitions
- native mobile animations
- desktop UI redraw cycles

Hyperion’s stability model is intentionally **platform-agnostic**.

The same test logic applies across:

- web
- mobile
- desktop
- hybrid contexts

Platform differences are handled by resolution, retries, and context management — not by branching tests.

---

## Common anti-patterns

Avoid:

- adding sleeps “to let animation finish”
- disabling animations globally just for tests
- branching test logic based on animation presence
- asserting transitional UI states

These patterns reduce test value and long-term maintainability.

---

## Key takeaways

- Animations are transient states, not test conditions
- Hyperion tolerates animation-related instability by design
- Tests should assert final, meaningful state
- Readiness belongs in widgets and Page Objects
- Sleeps and animation-specific waits are unnecessary

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Wait API and Timeouts](/docs/how-to/handle-waits-and-timeouts.md)  
→ Next: [Responsive (Viewport-Specific) Locators](/docs/how-to/responsive-locators.md)
