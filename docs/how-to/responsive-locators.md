← [Back to Documentation Index](/docs/index.md)  
← Previous: [Handling Animations and Dynamic Content](/docs/how-to/handle-animations.md)  
→ Next: [OS-Specific Locators](/docs/how-to/os-specific-locators.md)

---

# 4.4 Responsive Locators

Responsive (viewport-specific) locators let you keep **one logical Page Object** even when the UI layout changes across breakpoints.

Typical use cases:

- same feature, different DOM structure on small vs large viewports
- navigation collapsing into a menu on `xs/sm`
- table becoming a card list on `xs`
- button moving between toolbars depending on width

This guide explains how to declare viewport-specific locators in Hyperion and how to model responsive variation without branching your tests.

For background on the concept, see:  
`/docs/core-concepts/locator-resolution.md`

---

## When to use responsive locators

Use viewport-specific locators when:

- the *intent* stays the same, but the *layout* changes
- the element exists in different containers at different breakpoints
- there are multiple valid selectors depending on viewport width

Do not use responsive locators when:

- the element is static across layouts (use a single static locator)
- the variation is platform- or OS-driven (see 4.5 and 4.6)

---

## Viewport labels and breakpoints

Hyperion resolves viewport variation using predefined breakpoint labels.

Common labels include:

- `xs`, `sm`, `md`, `lg`, `xl`

Breakpoint boundaries come from configuration. The number of breakpoints is predefined, and boundaries can be adjusted in a test if needed.

This guide does not document configuration internals; it focuses on how to declare locators that participate in viewport resolution.

---

## The `default` fallback is viewport-only

Viewport variation supports a special fallback key: `default`.

- `default` applies to all viewports unless overridden
- specific breakpoints (like `xs`) override the `default` locator

Important:

- `default` is supported for viewport variation only
- platform- and OS-specific variation must be explicitly defined (no implicit fallback)

---

## Declaring a responsive `@element`

A responsive locator is declared by returning a mapping of viewport labels to locators.

```python
from selenium.webdriver.common.by import By
from hyperiontf.pages.decorators import element

class SearchResults:
    @element
    def search_input(self):
        return {
            "default": By.css_selector("<shared selector for most layouts>"),
            "xs": By.css_selector("<selector for the smallest layout>"),
            "md": By.css_selector("<selector for medium layout if it differs>"),
        }
```

Guidance:

- start with `default`
- override only the breakpoints that differ
- keep the mapping small and intention-focused

---

## Declaring responsive `@elements` collections

The same idea applies to `@elements` collections (lists, rows, items).

```python
from selenium.webdriver.common.by import By
from hyperiontf.pages.decorators import elements

class ResultsTable:
    @elements
    def rows(self):
        return {
            "default": By.css_selector("<desktop-table rows selector>"),
            "xs": By.css_selector("<mobile-card rows selector>"),
        }
```

The consumer code stays the same:

- you always call `rows`
- Hyperion resolves the correct locator for the active viewport at runtime

---

## How viewport is determined at runtime

Viewport resolution is runtime-based and depends on the active platform context:

- **web**: viewport dimensions are retrieved from the page (e.g., DOM/document viewport size)
- **mobile**: based on screen resolution and density
- **desktop**: based on window size

You do not need to compute these values manually in tests. You only declare how locators vary by breakpoint.

---

## Recommended modeling patterns

### Prefer stable widget boundaries
If layout changes affect a component, consider making it a widget and putting responsive variation inside it. This keeps Page Objects clean and isolates variability.

### Keep responsive variation local
Put viewport mappings on the element(s) that truly vary — avoid turning entire pages into “responsive maps”.

### Avoid responsive logic in tests
Tests should interact with behavior and resolved elements, not check viewport and pick selectors.

---

## Common mistakes

### Using `default` for platform or OS
`default` is for viewport variation only. Platform/OS must be explicit.

### Over-mapping everything
If only one element changes between `xs` and `md`, map only that element.

### Treating responsive locators as navigation
Responsive locators are for layout differences, not “page A vs page B” behavior.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Handling Animations and Dynamic Content](/docs/how-to/handle-animations.md)  
→ Next: [OS-Specific Locators](/docs/how-to/os-specific-locators.md)
