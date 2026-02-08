← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Button](/docs/reference/public-api/button.md)  
→ Next: [Components: DropDown](/docs/reference/public-api/dropdown.md)

---

# Component Spec: DropdownBySpec

`DropdownBySpec` defines the **declarative specification** for a dropdown component.

It is a **data-only specification object** used inside Page Objects to describe:
- the dropdown trigger (interaction target)
- the label / selected value source (optional)
- the dropdown options collection

`DropdownBySpec` extends `ButtonBySpec` and therefore supports the same
**trigger vs label separation**, allowing interaction and identity to be
decoupled when required.

---

## Public contract

### Constructor

```python
DropdownBySpec(
    root: LocatorTree,
    options: LocatorTree,
    label: Optional[LocatorTree] = None,
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
- as the fallback label source when `label` is not defined

---

### `label` (inherited)

**Type:** `Optional[LocatorTree]`  
**Required:** no  

Defines where the dropdown’s **visible label or selected value** should be
resolved from.

When omitted:
- the consuming component falls back to resolving text from `root`

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

This design supports modern UI frameworks that render menus via
overlays, portals, or document-level containers.

---

## Intended usage

`DropdownBySpec` is used inside Page Object declarations via the `@dropdown`
decorator.

### Basic dropdown (options under the same container)

```python
from hyperiontf import By, dropdown, DropdownBySpec


class SettingsPage(WebPage):

    @dropdown
    def language(self):
        return DropdownBySpec(
            root=By.id("language-select"),
            options=By.css("#language-select .option"),
        )
```

---

### Decoupled options (overlay / portal)

Some UI frameworks render dropdown menus outside of the trigger hierarchy
(e.g. document-level portals).

```python
from hyperiontf import By, dropdown, DropdownBySpec


class SettingsPage(WebPage):

    @dropdown
    def language(self):
        return DropdownBySpec(
            root=By.id("language-select"),
            options=By.css(".MuiPopover-root .MuiMenuItem-root"),
        )
```

In this configuration:
- the trigger is still resolved from `root`
- options are resolved independently using the provided locator

---

### Decoupled label (selected value not on the trigger)

Use `label` when the clickable trigger does not expose the selected value text.

```python
from hyperiontf import By, dropdown, DropdownBySpec


class SettingsPage(WebPage):

    @dropdown
    def language(self):
        return DropdownBySpec(
            root=By.id("language-select"),
            label=By.css(".selected-value"),
            options=By.css(".menu .option"),
        )
```

---

## Guarantees and non-goals

Hyperion guarantees:
- `DropdownBySpec` is treated as a declarative specification
- no element resolution occurs during Page Object construction
- the specification is preserved for use by the Dropdown component

`DropdownBySpec` does **not**:
- open or close the dropdown
- select options
- validate DOM relationships between trigger and options
- resolve options eagerly

Those responsibilities belong to the **Dropdown component**.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Button](/docs/reference/public-api/button.md)  
→ Next: [Components: DropDown](/docs/reference/public-api/dropdown.md)