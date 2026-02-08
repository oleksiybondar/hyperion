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

Optionally, a Dropdown may also define a **label source** that is separate from
the trigger element.

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
  - may or may not be the selected value source

### Dropdown options
Dropdown options are modeled as a **flat collection of elements**.

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
- `options` defines how option elements are located
- `label` (optional) defines where the selected value text is resolved from

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
- `options` selects option elements as descendants

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
If `root` is the trigger button, then a relative CSS selector would be evaluated
inside the button subtree, which cannot work.

### Modeling approaches

#### A) Use a relative XPath from the trigger (sibling traversal)

```python
DropdownBySpec(
    root=By.id("language-select"),
    options=By.xpath(
        "./following-sibling::ul[contains(@class, 'menu')]"
        "//li[contains(@class, 'language-option')]"
    ),
)
```

This keeps the locator anchored near the trigger and works when the menu
is a direct sibling.

#### B) Use document-scoped XPath (global)

```python
DropdownBySpec(
    root=By.id("language-select"),
    options=By.xpath(
        "//ul[contains(@class, 'menu')]"
        "//li[contains(@class, 'language-option')]"
    ),
)
```

This works regardless of where the menu is rendered, but the locator must be
specific enough to avoid matching unrelated menus.

---

## Scenario 3: Detached options (portal / overlay)

This is common in modern UI frameworks such as MUI, where menus are rendered
elsewhere in the DOM.

### DOM shape

```html
<button id="language-select">English</button>

<!-- rendered under <body> -->
<div class="MuiPopover-root">
  <ul>
    <li class="MuiMenuItem-root">English</li>
    <li class="MuiMenuItem-root">French</li>
  </ul>
</div>
```

### Modeling approaches

#### A) Use document-scoped XPath

Because options are detached from the trigger subtree, XPath with `//`
can be used to query from the document root:

```python
DropdownBySpec(
    root=By.id("language-select"),
    options=By.xpath("//li[contains(@class, 'MuiMenuItem-root')]"),
)
```

#### B) Use an explicit document-scoped locator (when available)

Hyperion may provide an explicit way to declare document-level scope:

```python
DropdownBySpec(
    root=By.id("language-select"),
    options=By.css(".MuiMenuItem-root").from_document(),
)
```

This makes global resolution an **explicit modeling decision**, rather than
an implicit XPath side effect.

---

## Selected value source

By default, the selected value is resolved from the **trigger element**.

If the UI renders the selected value elsewhere, a separate `label` locator
should be defined in `DropdownBySpec`.

```python
DropdownBySpec(
    root=By.id("language-select"),
    label=By.css(".selected-value"),
    options=By.css(".menu .option"),
)
```

Which source is appropriate is a **modeling decision** and should be documented
alongside the Page Object.

---

## Design guidelines

- Treat Dropdown as a **control**, not a container
- Do not assume options are children of the trigger
- Prefer explicit locators over implicit hierarchy
- Avoid artificial wrappers for modeling convenience
- If multiple dropdowns can coexist, ensure option locators are sufficiently specific

---

## Summary

Dropdown modeling in Hyperion is intentionally explicit:

- one trigger
- one flat collection of options
- optional decoupled label source
- no hierarchy assumptions

This approach supports real-world UI frameworks while keeping Page Objects
readable, reusable, and deterministic.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Component: RadioGroup](/docs/how-to/radiogroup.md)
→ Next: [Component: Table](/docs/how-to/table.md)