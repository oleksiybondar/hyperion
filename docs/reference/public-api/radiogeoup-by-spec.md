← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: DropDown](/docs/reference/public-api/dropdown.md)  
→ Next: [Components: RadioGroup](/docs/reference/public-api/radiogroup.md)

---

# Component Spec: RadioGroupBySpec

`RadioGroupBySpec` defines the **declarative specification** for a RadioGroup component.

It is a **data-only specification object** used inside Page Objects to describe:
- the radio group container
- the radio items collection
- optional per-item input and label structure
- an optional EQL expression used to determine **checked state** for custom radios

The spec is intentionally minimal.
Interaction and state resolution follow deterministic rules based on the presence
of `input`, `label`, and the item node itself.

---

## Public contract

### Constructor

```python
RadioGroupBySpec(
    root: LocatorTree,
    items: LocatorTree,
    input: Optional[LocatorTree] = None,
    label: Optional[LocatorTree] = None,
    checked_expression: Optional[str] = None,
)
```

---

## Fields

### `root`

**Type:** `LocatorTree`  
**Required:** yes  

Defines the effective container for the radio group.

The root is used to scope item resolution and to establish the logical ownership
of the RadioGroup within the Page Object hierarchy.

---

### `items`

**Type:** `LocatorTree`  
**Required:** yes  

Defines the radio **items collection**.

Important characteristics:
- items are modeled as a **flat collection**
- items are not required to be descendants of the group root
- the locator fully defines the resolution scope

Each resolved item represents a logical radio option and becomes the relative
scope for resolving `input` and `label`.

---

### `input`

**Type:** `Optional[LocatorTree]`  
**Required:** no  

Defines how to resolve a native radio input element relative to each item.

When provided:
- the resolved input node is treated as the **authoritative state source**
  for checked/unchecked evaluation
- the input may be hidden or not directly clickable

When omitted:
- checked-state evaluation falls back to the item node itself

---

### `label`

**Type:** `Optional[LocatorTree]`  
**Required:** no  

Defines how to resolve a label element relative to each item.

When present:
- the label may be used as a preferred interaction target
- the label may be used as the text/identity source for the item

When omitted:
- the item node itself may be used as the interaction and identity source

---

### `checked_expression`

**Type:** `Optional[str]`  
**Required:** no  

An optional **EQL boolean expression** used to determine which item is selected.

This field is intended for custom radio implementations where native input
semantics are not available or not reliable.

When provided:
- it becomes the authoritative checked-state strategy
- the expression is evaluated against a deterministic target node
  (see resolution order below)

When omitted:
- default/native radio semantics are sufficient

---

## Deterministic resolution order

For each resolved item, the RadioGroup component derives a **state node**
for checked-state evaluation in this order:

1) If `input` is defined, resolve the input relative to the item and use it  
2) Otherwise, use the item node itself

Checked-state evaluation **always** follows this order.

Interaction (click/tap) may additionally fall back to `label` or the item node
depending on platform and visibility, but this does not affect checked evaluation.

---

### Important: write EQL for the correct target node

`checked_expression` is evaluated against the resolved **state node**, not against
a composite structure.

This means:

- If `input` is defined, the expression is evaluated directly on the input node.  
  Do **not** write expressions such as `input.attribute:...` — there is no `input`
  child beneath the input node.

- If `input` is not defined, the expression is evaluated on the item node itself.  
  Do not reference input-only attributes unless the item node actually exposes them.

Correct examples:

- Wrapper carries state:
  `attribute:aria-checked == true`

- Input carries state:
  `attribute:checked == true`

---

## Intended usage

`RadioGroupBySpec` is used inside Page Object declarations via the `@radiogroup`
decorator.

### Standard radios (inputs visible)

```python
from hyperiontf import By, radiogroup, RadioGroupBySpec


class SettingsPage(WebPage):

    @radiogroup
    def theme(self):
        return RadioGroupBySpec(
            root=By.id("theme"),
            items=By.css("input[type='radio']"),
        )
```

---

### Hidden inputs with clickable labels

```python
from hyperiontf import By, radiogroup, RadioGroupBySpec


class SettingsPage(WebPage):

    @radiogroup
    def theme(self):
        return RadioGroupBySpec(
            root=By.id("theme"),
            items=By.css(".radio-item"),
            input=By.css("input[type='radio']"),
            label=By.css("label"),
        )
```

---

### Custom radios with checked expression (wrapper carries state)

Use this pattern when checked state is stored on the item wrapper (for example via ARIA):

```python
from hyperiontf import By, radiogroup, RadioGroupBySpec


class SettingsPage(WebPage):

    @radiogroup
    def theme(self):
        return RadioGroupBySpec(
            root=By.id("theme"),
            items=By.css("[role='radio']"),
            checked_expression="attribute:aria-checked == true",
        )
```

---

### Custom radios with checked expression (input carries state)

Use this pattern when the underlying input exists and is the correct state source:

```python
from hyperiontf import By, radiogroup, RadioGroupBySpec


class SettingsPage(WebPage):

    @radiogroup
    def theme(self):
        return RadioGroupBySpec(
            root=By.id("theme"),
            items=By.css(".radio-item"),
            input=By.css("input[type='radio']"),
            checked_expression="attribute:checked == true",
        )
```

Because `input` is defined, the expression is evaluated on the input node directly.

---

## Guarantees and non-goals

Hyperion guarantees:
- `RadioGroupBySpec` is treated as a declarative specification
- no element resolution occurs during Page Object construction
- the specification is preserved verbatim for use by the RadioGroup component
- if `checked_expression` is provided, it is evaluated against the state node
  determined by the resolution order above

`RadioGroupBySpec` does **not**:
- select a radio option
- resolve items eagerly
- validate DOM relationships between group, items, input, and label

Those responsibilities belong to the **RadioGroup component**.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: DropDown](/docs/reference/public-api/dropdown.md)  
→ Next: [Components: RadioGroup](/docs/reference/public-api/radiogroup.md)