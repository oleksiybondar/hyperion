← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Button](/docs/reference/public-api/button.md)  
→ Next: [Components: DropDown](/docs/reference/public-api/dropdown.md)

---

# Component Spec: DropdownBySpec

`DropdownBySpec` defines the **declarative specification** for a Dropdown component.

It is a **data-only specification object** used inside Page Objects to describe:
- the dropdown trigger (interaction target)
- the dropdown options collection
- optional separation of interaction and identity (label)
- optional option-level label resolution (`option_label`)
- the **selected value resolution strategy**

`DropdownBySpec` extends `ButtonBySpec` and therefore supports the same
**trigger vs label separation**, allowing interaction and selected-value
resolution to be decoupled when required.

---

## Public contract

### Constructor

```python
DropdownBySpec(
    root: LocatorTree,
    options: LocatorTree,
    label: Optional[LocatorTree] = None,
    value_attribute: Optional[str] = "AUTO",
    option_label: Optional[LocatorTree] = None,
)
```

---

## Fields

### `root` (inherited)

**Type:** `LocatorTree`  
**Required:** yes  

Defines the primary **interaction target** for the dropdown (the trigger).

The consuming component uses `root`:
- to open and close the dropdown
- as a potential source of the selected value
- as the fallback label source when `label` is not defined

---

### `label` (inherited)

**Type:** `Optional[LocatorTree]`  
**Required:** no  

Defines where the dropdown’s **visible label or selected value** should be
resolved from.

When provided:
- the label element may act as the selected value source
- the trigger element remains the interaction target

When omitted:
- the consuming component falls back to resolving text or value from `root`,
  depending on the selected value resolution strategy.

This field exists to support UIs where the selected value is rendered by a
nested or separate element.

---

### `options`

**Type:** `LocatorTree`  
**Required:** yes  

Defines the dropdown options collection.

Important characteristics:
- options are modeled as a **flat collection**
- options are **not required** to be descendants of the trigger
- the locator fully defines the resolution scope

This design supports modern UI frameworks that render menus via overlays,
portals, or document-level containers.

At runtime, options are consumed as `Button` components by Dropdown.

---

### `option_label`

**Type:** `Optional[LocatorTree]`  
**Required:** no  

Defines where each option's visible text/label should be resolved from.

Use this when:
- the clickable option container does not expose meaningful text directly
- option text is rendered by a nested child element

When omitted, option text is resolved from the option root.

---

### `value_attribute`

**Type:** `Optional[str]`  
**Required:** no  
**Default:** `"AUTO"`

Defines how the **currently selected value** should be resolved.

Supported values:

- `"AUTO"` (default)  
  Use heuristic resolution based on the underlying control type.

  Typical behavior:
  - native `<select>` / `<input>` → resolve selected value via `"value"` attribute
  - JavaScript-driven dropdowns → resolve visible text from `label` or `root`

- `"text"`  
  Always resolve the selected value using visible text
  (from `label` if defined, otherwise from `root`).

- any valid DOM attribute name  
  Resolve the selected value by reading the specified attribute
  (e.g. `"value"`, `"aria-label"`, `"data-value"`).

This field allows explicit override of heuristic behavior when automatic
resolution is insufficient or ambiguous.

---

## Intended usage

`DropdownBySpec` is used inside Page Object declarations via the `@dropdown`
decorator.

### Basic dropdown (heuristic value resolution)

```python
from hyperiontf import By, dropdown, DropdownBySpec


class SettingsPage(WebPage):

    @dropdown
    def language(self):
        return DropdownBySpec(
            root=By.id("language-select"),
            options=By.css(".language-option"),
        )
```

---

### Explicit value resolution via attribute

Use this when the selected value must be read from a specific attribute.

```python
from hyperiontf import By, dropdown, DropdownBySpec


class SettingsPage(WebPage):

    @dropdown
    def language(self):
        return DropdownBySpec(
            root=By.id("language-select"),
            options=By.css(".language-option"),
            value_attribute="value",
        )
```

---

### Decoupled label with text-based resolution

```python
from hyperiontf import By, dropdown, DropdownBySpec


class SettingsPage(WebPage):

    @dropdown
    def language(self):
        return DropdownBySpec(
            root=By.id("language-select"),
            label=By.css(".selected-value"),
            options=By.css(".menu .option"),
            option_label=By.css(".option-text"),
            value_attribute="text",
        )
```

---

## Guarantees and non-goals

Hyperion guarantees:
- `DropdownBySpec` is treated as a declarative specification
- no element resolution occurs during Page Object construction
- the specification is preserved verbatim for use by the Dropdown component
- selected value resolution follows the declared or heuristic strategy

`DropdownBySpec` does **not**:
- open or close the dropdown
- select options
- resolve the selected value eagerly
- validate DOM relationships between trigger and options

Those responsibilities belong to the **Dropdown component**.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Button](/docs/reference/public-api/button.md)  
→ Next: [Components: DropDown](/docs/reference/public-api/dropdown.md)
