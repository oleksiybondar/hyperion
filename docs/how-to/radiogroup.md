← [Back to Documentation Index](/docs/index.md)  
← Previous: [Elements Query Language (EQL) Recipes](/docs/how-to/eql-recipes.md)  
→ Next: [Component: Dropdown](/docs/how-to/dropdown.md)

---

# RadioGroup

This guide describes how to model **reusable RadioGroup widgets** in Hyperion using
**typed locator specification objects** and **high-level intent decorators**.

It focuses on **Page Object structure and locator design**, not on test logic or API calls.
Readers are expected to be familiar with Hyperion Page Objects, `By` locators, and relative
selector scoping.

> This document describes the intended usage pattern for reusable RadioGroup widgets.  
> The underlying implementation will follow this contract.

---

## Why RadioGroup needs a spec-based model

Radio groups are conceptually simple, but their DOM structure varies widely in real
applications:

- items may or may not have a wrapper
- `<label>` may wrap `<input>` or be a sibling
- groups may or may not have a dedicated container
- React fragments often remove otherwise useful structure

Because of this variability, a reusable RadioGroup cannot assume a fixed internal layout.

Hyperion models RadioGroup structure explicitly via a **typed locator specification**
(`RadioGroupBySpec`) rather than hardcoding assumptions.

---

## Core concepts

### RadioGroup
A **RadioGroup** represents a logical group of radio options.

- Declared on a Page Object using the `@radiogroup` decorator
- Configured via a `RadioGroupBySpec` returned from the property
- Scoped by a meaningful group root (form, fieldset, section, etc.)

### RadioItem
A **RadioItem** represents one logical option in the group.

A RadioItem consists of:
- a **state source** (the radio input)
- an optional **label** (click target and text source)

A RadioItem **does not require a wrapper element**.

---

## Declaring a RadioGroup

A RadioGroup is declared by returning a `RadioGroupBySpec` from a Page Object property.

Conceptually:

- `root` defines the group scope
- `items` defines how individual radio items are located
- `input` and `label` are resolved **relative to each item**

```python
from hyperiontf import By, radiogroup, RadioGroupBySpec, WebPage


class SettingsPage(WebPage):

    @radiogroup
    def notifications(self) -> RadioGroupBySpec:
        return RadioGroupBySpec(
            root=By.id("notifications"),
            items=By.css("label"),
            input=By.xpath("./input"),
            label=By.xpath("./"),
        )
```

The exact behavior API is documented elsewhere.  
This guide focuses only on **how to model the structure correctly**.

---

## Scenario 1: Item wrapper exists (simplest case)

### DOM shape

```html
<div id="notifications">
  <div class="item">
    <input type="radio" name="n" />
    <label>Email</label>
  </div>
  <div class="item">
    <input type="radio" name="n" />
    <label>SMS</label>
  </div>
</div>
```

### Modeling approach

- `items` selects the wrapper
- `input` and `label` are resolved relative to it

```python
RadioGroupBySpec(
    root=By.id("notifications"),
    items=By.css(".item"),
    input=By.css("input"),
    label=By.css("label"),
)
```

This is the most straightforward case and requires no XPath tricks.

---

## Scenario 2: `<label>` wraps `<input>` (or vice-versa)

### DOM shape (label wraps input)

```html
<div id="notifications">
  <label>
    <input type="radio" name="n" />
    Email
  </label>
  <label>
    <input type="radio" name="n" />
    SMS
  </label>
</div>
```

### Key idea: choose the correct item root

In this structure:
- the `<label>` *is* the RadioItem
- the label text is the identity
- the input is nested inside

### Modeling approach

- `items` selects `<label>`
- `label` is the item root itself
- `input` is resolved relative to it
- XPath `./` is used as a **self selector**

```python
RadioGroupBySpec(
    root=By.id("notifications"),
    items=By.css("label"),
    input=By.xpath("./input"),
    label=By.xpath("./"),
)
```

This works regardless of whether the input is before or after the text.

> XPath `./` is the most reliable cross-backend way to reference the current element.  
> CSS does not provide a universally supported equivalent.

---

## Scenario 3: No item wrapper, no nesting (sibling pairing)

### DOM shape

```html
<form id="notifications">
  <input type="radio" id="n1" name="n" />
  <label for="n1">Email</label>

  <input type="radio" id="n2" name="n" />
  <label for="n2">SMS</label>
</form>
```

This is common in real applications and React output.

### Modeling constraints

- There is **no item wrapper**
- Input and label are siblings
- Group scope still exists (form)

### Modeling approach

- `root` scopes the group
- `items` selects **inputs**
- input is the RadioItem root
- label is resolved via sibling XPath

```python
RadioGroupBySpec(
    root=By.id("notifications"),
    items=By.css("input[type='radio']"),
    input=By.xpath("./"),
    label=By.xpath("./following-sibling::label[1]"),
)
```

Notes:
- XPath indices are **1-based**
- `following-sibling::label[1]` selects the nearest matching label
- The input is always the **state source**

The reverse pattern (label before input) can be handled with
`preceding-sibling::label[1]`.

---

## Label is optional

In some UIs:
- radios have no visible `<label>`
- identity comes from attributes (`value`, `aria-label`, `data-*`)
- or the root element text itself

RadioGroup supports this by treating `label` as optional.

If no label is defined:
- the item root becomes the identity source
- text-based selection relies on the root element

Which identity source is appropriate should be decided per project and documented
alongside the Page Object.

---

## Design guidelines

- Prefer **explicit structure** over framework guessing
- Always scope RadioGroup to a meaningful container
- Choose the RadioItem root based on DOM reality, not ideal markup
- Use XPath relative selectors (`./`, `following-sibling::`) when structure demands it
- Avoid introducing pseudo wrappers just to satisfy modeling

---

## Summary

RadioGroup modeling in Hyperion is:
- explicit
- spec-driven
- resilient to real-world DOM variations

By choosing the correct item root and using relative locators, you can model even
non-ideal markup cleanly while keeping Page Objects readable and reusable.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Logging and Reporting](/docs/how-to/logging-and-reports.md) 
→ Next: [Component: Dropdown](/docs/how-to/dropdown.md)
