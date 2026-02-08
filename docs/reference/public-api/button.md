← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Button Specification](/docs/reference/public-api/button-by-spec.md)  
→ Next: [Components: DropDown Specification](/docs/reference/public-api/dropdown-by-spec.md)

---

# Component: Button

`Button` is a reusable clickable component in Hyperion.

It behaves like an ordinary element in almost all respects, but is backed by a
`ButtonBySpec` specification that allows the component to decouple:
- the interaction target (click target)
- the label / visible text source (optional)

This exists to support UIs where the clickable container does not expose
meaningful text (common in desktop automation trees and complex markup).

---

## Declaration

A Button is declared in a Page Object using the `@button` decorator and a
`ButtonBySpec`.

```python
from hyperiontf import By, button, ButtonBySpec, WebPage


class SettingsPage(WebPage):

    @button
    def save(self):
        return ButtonBySpec(
            root=By.id("save"),
        )
```

---

## Relationship to Element / Widget

`Button` is a UI component that uses the same interaction model as standard
elements/widgets (clicking, presence/visibility checks, expectations, etc.).

It exists primarily to provide a stable abstraction for **text resolution**
when the label is not on the clickable root.

---

## Text resolution

### `get_text(log: bool = True) -> str`

`Button.get_text()` follows this contract:

- If the underlying `ButtonBySpec` defines `label`,
  the Button resolves text from the label element.
- Otherwise, text resolution falls back to the default element/widget behavior
  (the same behavior you would get from an ordinary element).

This makes text resolution deterministic and consistent across backends.

---

## Example: decoupled label

Use a label locator when the clickable element does not expose meaningful text.

```python
from hyperiontf import By, button, ButtonBySpec, WebPage


class SettingsPage(WebPage):

    @button
    def save(self):
        return ButtonBySpec(
            root=By.id("save-button"),
            label=By.css(".button-label"),
        )
```

In this configuration:
- clicks are performed on `root`
- text is resolved from `label`

---

## Guarantees and non-goals

Hyperion guarantees:
- Button uses `ButtonBySpec.root` as the component root / click target
- Button resolves text from `ButtonBySpec.label` when it is provided
- when `label` is not provided, Button behaves like an ordinary element/widget

Button does **not**:
- impose a required DOM structure
- require that label is a child of root
- perform eager resolution during Page Object construction

---

## See also

- [Element API ref](/docs/reference/public-api/element.md)

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Button Specification](/docs/reference/public-api/button-by-spec.md)  
→ Next: [Components: DropDown Specification](/docs/reference/public-api/dropdown-by-spec.md)