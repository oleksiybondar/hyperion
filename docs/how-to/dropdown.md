← [Back to Documentation Index](/docs/index.md)  
← Previous: [Component: RadioGroup](/docs/how-to/radiogroup.md)  
→ Next: [Component: Table](/docs/how-to/table.md)

---

# Dropdown

This guide describes how to model **reusable Dropdown widgets** in Hyperion using
**typed locator specification objects** and a **high-level intent decorator**.

It focuses on **Page Object structure and locator design**, not on test logic
or Dropdown interaction APIs.

Readers are expected to be familiar with Hyperion Page Objects, `By` locators,
relative selector scoping, and advanced DOM modeling concepts.

> This document describes the intended usage pattern for reusable Dropdown widgets.  
> The underlying implementation follows this contract.

---

## What a Dropdown represents

In Hyperion terms, a **Dropdown** is a control composed of:

- a **trigger element** that:
  - receives interaction
  - opens and closes the menu
- a collection of **options** that:
  - may appear anywhere in the DOM
  - are not required to be children of the trigger
  - are resolved explicitly via locators

Optionally, a Dropdown may also define:
- a **label source** that is separate from the trigger element
- a **selected value resolution strategy** that controls how the current value
  is read from the UI

Anything that does not follow this mental model (e.g. searchable inputs,
autocomplete fields, async selectors) is **not considered a Dropdown** and should
be modeled as a different widget.

---

## Core concepts

### Dropdown

A **Dropdown** is a logical control with a single trigger.

- Declared on a Page Object using the `@dropdown` decorator
- Configured via a `DropdownBySpec` returned from the property
- The trigger element:
  - is the interaction target
  - may or may not be the selected value source, depending on the
    selected value resolution strategy

---

### Dropdown options

Dropdown options are modeled as a **flat collection of Button-compatible components**.

- Options do **not** need to be children of the trigger
- Options may be:
  - inline
  - siblings
  - rendered in a portal
  - rendered under the document root
- Scoping is controlled by the **locator**, not by widget hierarchy

There is no required “options wrapper”.

---

## Declaring a Dropdown

A Dropdown is declared by returning a `DropdownBySpec` from a Page Object property.

Conceptually:
- `root` defines the trigger
- `options` defines how option components are located
- `label` (optional) defines where the selected value text is resolved from
- `option_label` (optional) defines where each option's text is resolved from

```python
from hyperiontf import By, dropdown, DropdownBySpec, WebPage


class SettingsPage(WebPage):

    @dropdown
    def language(self) -> DropdownBySpec:
        return DropdownBySpec(
            root=By.id("language-select"),
            options=By.css(".language-option"),
        )
```

This guide intentionally avoids showing interaction methods.
Only **structure and locator modeling** are covered here.

---

## Scenario 1: Options inline with the trigger

### DOM shape

```html
<div id="language-select">
  English
  <ul>
    <li class="language-option">English</li>
    <li class="language-option">French</li>
  </ul>
</div>
```

### Modeling approach

- `root` selects the trigger
- `options` selects option components as descendants

```python
DropdownBySpec(
    root=By.id("language-select"),
    options=By.css(".language-option"),
)
```

This is the simplest case and works with pure relative scoping.

---

## Scenario 2: Options rendered as siblings

### DOM shape

```html
<button id="language-select">English</button>

<ul class="menu">
  <li class="language-option">English</li>
  <li class="language-option">French</li>
</ul>
```

### Why CSS alone may not work

By default, Hyperion resolves locators **relative to the widget root**.
If `root` is the trigger button, a relative CSS selector would be evaluated
inside the button subtree, which cannot work.

### Modeling approaches

#### A) Use a relative XPath from the trigger

```python
DropdownBySpec(
    root=By.id("language-select"),
    options=By.xpath(
        "./following-sibling::ul[contains(@class, 'menu')]"
        "//li[contains(@class, 'language-option')]"
    ),
)
```

#### B) Use document-scoped XPath

```python
DropdownBySpec(
    root=By.id("language-select"),
    options=By.xpath(
        "//ul[contains(@class, 'menu')]"
        "//li[contains(@class, 'language-option')]"
    ),
)
```

---

## Scenario 3: Detached options (portal / overlay)

### DOM shape

```html
<button id="language-select">English</button>

<div class="MuiPopover-root">
  <ul>
    <li class="MuiMenuItem-root">English</li>
    <li class="MuiMenuItem-root">French</li>
  </ul>
</div>
```

### Modeling approaches

#### A) Document-scoped XPath

```python
DropdownBySpec(
    root=By.id("language-select"),
    options=By.xpath("//li[contains(@class, 'MuiMenuItem-root')]"),
)
```

#### B) Explicit document-scoped locator (recommended)

```python
DropdownBySpec(
    root=By.id("language-select"),
    options=By.css(".MuiMenuItem-root").from_document(),
)
```

This makes global resolution an **explicit modeling decision**, rather than an
implicit XPath side effect.

---

## Selected value resolution

Dropdown implementations differ significantly in how the selected value is exposed.

Hyperion models this explicitly using the `value_attribute` field on
`DropdownBySpec`.

This controls how `selected_value`, `assert_selected_value`, and related APIs
resolve the current dropdown value.

---

### Resolution strategies

#### `"AUTO"` (default)

Heuristic resolution based on the underlying control.

Typical behavior:
- native `<select>` or `<input>`  
  → resolve selected value via the `"value"` attribute
- JavaScript-driven dropdowns  
  → resolve visible text from `label` or `trigger`

```python
DropdownBySpec(
    root=By.id("language-select"),
    options=By.css(".option"),
)
```

---

#### `"text"`

Always resolve the selected value using visible text.

```python
DropdownBySpec(
    root=By.id("language-select"),
    option_label=By.css(".language-option__text"),
    label=By.css(".selected-value"),
    options=By.css(".option"),
    value_attribute="text",
)
```

---

#### Explicit DOM attribute

Resolve the selected value from a specific DOM attribute.

Common examples include `"value"`, `"aria-label"`, or `"data-value"`.

```python
DropdownBySpec(
    root=By.id("language-select"),
    options=By.css(".option"),
    value_attribute="value",
)
```

---

## Design guidelines

- Treat Dropdown as a **control**, not a container
- Do not assume options are children of the trigger
- Prefer explicit locators over implicit hierarchy
- Prefer `value_attribute="AUTO"` unless a specific override is required
- If multiple dropdowns coexist, ensure option locators are sufficiently specific

---

## Summary

Dropdown modeling in Hyperion is intentionally explicit:

- one trigger
- one flat collection of options
- optional decoupled label
- optional decoupled option label
- explicit selected value resolution strategy
- no hierarchy assumptions

This approach supports real-world UI frameworks while keeping Page Objects
readable, reusable, and deterministic.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Component: RadioGroup](/docs/how-to/radiogroup.md)  
→ Next: [Component: Table](/docs/how-to/table.md)
