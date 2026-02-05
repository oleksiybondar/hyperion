← [Back to Documentation Index](/docs/index.md)  
← Previous: [Locator Resolution Order](/docs/reference/behavior-contracts/locator-resolution.md)  
→ Next: [Retry and Timeout Semantics](/docs/reference/behavior-contracts/timeouts.md)

---

# 6.2 Context Switching Rules

This page defines **guarantees** for Hyperion’s automatic context and content switching when interacting with elements across:

- main document vs iframe documents (web)
- native content vs web content (mobile hybrid / webview)

Hyperion’s goal is that **element resolution and interaction occur in the correct context automatically**, based on the Page Object hierarchy.

---

## Context boundaries

Hyperion treats these as context boundaries:

- **Document vs IFrame document** (web)
- **Native context vs Web content** (webview/hybrid)

The framework also distinguishes “default content” equivalents (e.g., default document, native context) as the baseline context.

---

## Automatic switching is the default

Guarantee:

- Hyperion automatically selects the correct context required to resolve and interact with an element.

This applies to:

- locating elements
- interacting (click, fill, etc.)
- resolving nested structures (page → widget → iframe → element, etc.)

---

## Switching is demand-driven during resolution

Hyperion switches context **only when needed**, based on the Page Object “virtual DOM” structure:

- Page Objects and widgets are static Python objects.
- Each element wrapper carries the locator and a relationship to its parent scope.
- Hyperion uses this hierarchy to determine which context the element belongs to.

Guarantee:

- When resolving a chain like `page.a.b.c`, Hyperion may switch contexts **multiple times** while walking the chain, selecting the correct context for each step.

Example (conceptual):

- resolve `a` in default content
- resolve `b` inside iframe `b` (switch to iframe context)
- resolve `c` inside that iframe (stay in iframe context)

---

## No global “always restore” behavior

Hyperion does **not** restore context after every action as a general rule.

Guarantee:

- Context switching occurs when accessing or resolving an element that belongs to a different context than the currently selected one.

In other words:

- If the next action targets an element in the same context, no switching occurs.
- If the next action targets an element in another context (e.g., default document vs iframe, native vs web), Hyperion switches at that point.

---

## Manual context switching

Manual content/context switching is **possible** but **discouraged**.

Guidance (contract-level intent):

- Tests and Page Objects should prefer declarative structure (IFrame/WebView objects and nesting) over manual switching.
- Manual switching may reduce stability and makes logs and failures harder to interpret.

---

## Stale recovery may force a context refresh

In stale-recovery scenarios, Hyperion may re-assert or refresh the expected context to ensure the selected context matches the current runtime state.

Guarantee:

- Hyperion preserves correct scope and context during recovery by re-resolving elements from their parent scope in the Page Object hierarchy.

(See `/docs/reference/behavior-contracts/timeouts.md` for retry and stale recovery semantics.)

---

## Related documentation

- Locator resolution order: `/docs/reference/behavior-contracts/locator-resolution.md`
- Retry and timeout semantics: `/docs/reference/behavior-contracts/timeouts.md`
- Cross-platform example with WebView usage: `/docs/examples/patterns/cross-platform-calculator.md`

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Locator Resolution Order](/docs/reference/behavior-contracts/locator-resolution.md)  
→ Next: [Retry and Timeout Semantics](/docs/reference/behavior-contracts/timeouts.md)
