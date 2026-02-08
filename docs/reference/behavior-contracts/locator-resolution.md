← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Tabs](/docs/reference/public-api/tabs.md)  
→ Next: [Behavior Contracts: Context Switching Rules](/docs/reference/behavior-contracts/context-switching.md)

---

# 6.1 Locator Resolution Order

This page defines **guarantees** for how Hyperion resolves locators into concrete backend selectors at runtime.

These rules apply equally to `@element`, `@elements`, widgets, and any other Page Object locator declarations.

---

## Key terms

- **Locator**: a backend-specific selector (e.g., `By.id(...)`, `By.css_selector(...)`).
- **Locator mapping**: a nested `dict` that contains alternative locators for different runtime contexts.

---

## Supported resolution dimensions

Hyperion resolves locator mappings using these dimensions (in order):

1. **Platform** (`"web" | "mobile" | "desktop"`)
2. **OS** (`"Windows" | "Darwin" | "Linux" | "Android" | "iOS"`)
3. **Viewport breakpoint** (responsive locators; breakpoint labels are config-driven)

---

## Resolution order and rules

### Rule 1: Non-dict locators are used as-is
If a locator declaration returns a value that is **not** a `dict`, Hyperion uses it directly without resolution.

```python
@element
def title(self):
    return By.css_selector("h1")
```

### Rule 2: Dict locators are resolved by exclusion, in a fixed order
If a locator declaration returns a `dict`, Hyperion resolves it by selecting the applicable branch at runtime in this order:

**platform → OS → viewport**

This resolution is applied **recursively** until a non-dict locator is produced.

Important guarantee:

- **Dict nesting order does not affect correctness**: Hyperion resolves mappings recursively using the applicable runtime context and a method-of-exclusion approach.

---

## Fast-fail behavior (missing branches)

If a dict-locator does not contain a required branch for the current runtime context, Hyperion **fails fast**.

Examples of fast-fail conditions:

- platform key is missing for the active platform
- OS key is missing under the active platform
- viewport key is missing when viewport mapping is used

Hyperion does **not** treat missing mapping branches as “element not found until timeout”. Missing branches are a configuration/declaration error and fail immediately.

---

## Viewport resolution rules (responsive locators)

Viewport resolution is applied **after** platform and OS selection (when the locator mapping includes viewport breakpoints).

### No implicit viewport fallback
Viewport mappings **do not** use `default` fallback.

Guarantee:

- If a viewport-specific mapping does not contain the current breakpoint key, resolution **fails fast**.

(Responsive breakpoint thresholds are configuration-driven; see `/docs/how-to/responsive-locators.md` for usage guidance.)

---

## Example: platform + OS + viewport mapping shape

This example shows the intended mapping shape. Values are illustrative.

```python
@element
def result(self):
    return {
        "web": {
            "xs": By.id("<web xs result>"),
            "md": By.id("<web md result>"),
        },
        "mobile": {
            "Android": By.id("<android result>"),
            "iOS": By.predicate("<ios result predicate>"),
        },
        "desktop": {
            "Windows": By.name("<windows result name>"),
            "Darwin": By.predicate("<mac result predicate>"),
        },
    }
```

Notes:

- web uses viewport breakpoints
- mobile/desktop use OS branches
- if the active branch is missing, Hyperion fails fast

---

## Related documentation

- Responsive locators: `/docs/how-to/responsive-locators.md`
- OS-specific locators: `/docs/how-to/os-specific-locators.md`
- Platform-agnostic locators: `/docs/how-to/platform-agnostic-locators.md`

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Tabs](/docs/reference/public-api/tabs.md)  
→ Next: [Behavior Contracts: Context Switching Rules](/docs/reference/behavior-contracts/context-switching.md)
