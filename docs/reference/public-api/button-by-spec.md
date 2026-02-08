← [Back to Documentation Index](/docs/index.md)  
← Previous: [Logger](/docs/reference/public-api/logger.md)  
→ Next: [Components: Button](/docs/reference/public-api/button.md)

---

# Component Spec: ButtonBySpec

`ButtonBySpec` defines the **declarative specification** for a button-like,
clickable UI component in Hyperion.

It is a **data-only specification object** used inside Page Objects to describe:
- which element receives user interaction
- which element provides the visible label or identity (optional)

`ButtonBySpec` exists to support real-world UI structures where the clickable
element and the visible label are not the same node.

---

## Public contract

### Constructor

```python
ButtonBySpec(
    root: LocatorTree,
    label: Optional[LocatorTree] = None,
)
```

---

## Fields

### `root`

**Type:** `LocatorTree`  
**Required:** yes  

Defines the primary **interaction target** for the button component.

The consuming component uses `root`:
- as the effective component root
- as the click target
- as the fallback text source when `label` is not defined

---

### `label`

**Type:** `Optional[LocatorTree]`  
**Required:** no  

Defines where the button’s **label or visible text** should be resolved from.

When provided:
- text resolution is delegated to the label element
- the label may be a child, sibling, or descendant of the root

When omitted:
- the consuming component falls back to resolving text from the root element

---

## Intended usage

`ButtonBySpec` is used **only** inside Page Object declarations
via the `@button` decorator.

### Simple button (text on root)

```python
from hyperiontf import By, button, ButtonBySpec


class MyPage(WebPage):

    @button
    def submit(self):
        return ButtonBySpec(
            root=By.id("submit"),
        )
```

---

### Decoupled trigger and label

Use this pattern when the clickable container does not expose meaningful text
(e.g. desktop UI trees, complex markup, nested text nodes).

```python
from hyperiontf import By, button, ButtonBySpec


class MyPage(WebPage):

    @button
    def save(self):
        return ButtonBySpec(
            root=By.id("save-button"),
            label=By.css(".button-label"),
        )
```

---

## Guarantees and non-goals

Hyperion guarantees:
- `ButtonBySpec` is treated as a declarative specification
- no element resolution occurs during Page Object construction
- the specification is preserved for use by the Button component

`ButtonBySpec` does not:
- locate elements
- perform clicks
- resolve text eagerly
- validate DOM structure

Those responsibilities belong to the **Button component**.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Logger](/docs/reference/public-api/logger.md)  
→ Next: [Components: Button](/docs/reference/public-api/button.md)