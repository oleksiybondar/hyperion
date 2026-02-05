← [Back to Documentation Index](/docs/index.md)  
← Previous: [Retry and Timeout Semantics](/docs/reference/behavior-contracts/timeouts.md)  
→ Next: [Cross-Platform Calculator Example](/docs/examples/patterns/cross-platform-calculator.md)

---

# 6.4 Logging Behavior

This page defines **guarantees** for Hyperion logging as it relates to:

- test cases and fixtures
- Page Object method calls
- expectations and verifications
- readability and traceability of failures

The goal of Hyperion logging is not only to report failures, but to explain *what happened* in a way that supports fast diagnosis.

---

## Test case metadata

Guarantee:

- Each test case produces logs associated with the test case name.
- The test case docstring is used as the descriptive header text in the HTML log output (when present).

---

## Automatic call grouping (push/pop “folders”)

Guarantee:

- User-defined Page Object methods are automatically wrapped at instantiation time so logs include “push/pop” grouping entries.
- This grouping enables expand/collapse style viewing so the reader can focus on high-level flow first and drill into details as needed.
- Group names are derived from the method name in a human-readable way.

This applies to Page Object methods you define (not framework-internal methods).

---

## `expect(...)` vs `verify(...)`

Guarantee:

- `expect(...)` and `verify(...)` produce the same structured logging output format, but with different semantics and marking.

### `expect(...)`
- Represents an assertion.
- Failing `expect(...)` is a test failure.
- Logs include detailed comparison information.

### `verify(...)`
- Used for decision logging and diagnostics.
- Does not replace assertions and must not be treated as a “soft assert”.
- Allows tests and flows to log why a branch was taken without changing pass/fail outcome.

(For usage guidance, see `/docs/how-to/write-stable-tests.md` and the examples in `/docs/examples/patterns/cross-platform-calculator.md`.)

---

## Detail level guarantee

Guarantee:

- Hyperion logging aims for maximal detail for comparisons and expectation outcomes.
- This is a core reason Hyperion provides its own `expect`/`verify` objects rather than delegating to third-party equivalents.

---

## Fixture logging

Guarantee:

- Hyperion provides fixture-level logging integration (e.g., via a pytest fixture wrapper) so fixture execution is visible in the log structure alongside Page Object method calls and test steps.

---

## What this page does not specify

This contract page does not specify:

- exact log rendering format details (HTML structure, CSS, etc.)
- internal logger implementation
- integration mechanics with external tool logs

It specifies only the behavioral guarantees: what is logged and how it is structured conceptually.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Retry and Timeout Semantics](/docs/reference/behavior-contracts/timeouts.md)  
→ Next: [Cross-Platform Calculator Example](/docs/examples/patterns/cross-platform-calculator.md)
