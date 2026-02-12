← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: DropDown Specification](/docs/reference/public-api/dropdown-by-spec.md)  
→ Next: [Components: RadioGroup Specification](/docs/reference/public-api/radiogroup-by-spec.md)

---

# Component: Dropdown

`Dropdown` is an interactive selection component in Hyperion.

It represents a control composed of:
- a clickable **trigger** (inherited from `Button`)
- a dynamically resolved collection of **options**

`Dropdown` builds on the `Button` component and extends it with:
- explicit open / close semantics
- option discovery and selection
- expressive selection via index, text, or pattern
- configurable selected value resolution
- verification and assertion helpers

---

## Declaration

A Dropdown is declared in a Page Object using the `@dropdown` decorator
and configured via a `DropdownBySpec`.

```python
from hyperiontf import By, dropdown, DropdownBySpec, WebPage


class SettingsPage(WebPage):

    @dropdown
    def language(self):
        return DropdownBySpec(
            root=By.id("language-select"),
            options=By.css(".language-option"),
        )
```

---

## Relationship to Button

`Dropdown` inherits from `Button` and therefore:
- uses the same trigger / label resolution model
- supports decoupled label sources
- behaves like an ordinary clickable element where applicable

In addition, `Dropdown`:
- manages a dynamic options collection
- resolves the currently selected value according to the specification
- exposes selection-specific APIs

---

## Open / close semantics

### `open_dropdown()`

Opens the dropdown if it is not already open.

This method is idempotent and safe to call multiple times.

---

### `close_dropdown()`

Closes the dropdown if it is currently open.

This method is idempotent and safe to call multiple times.

---

### `are_options_opened -> bool`

Indicates whether dropdown options are currently rendered and visible.

This property reflects **runtime UI state**, not static structure.

---

## Selecting options

### `select(option)`

Selects a dropdown option.

Supported selector types:
- `int` — select by index
- `str` — select by exact text match
- `re.Pattern` — select by text pattern

```python
language.select(0)
language.select("English")
language.select(r"Eng.*")
```

Selection is performed by:
- opening the dropdown (if needed)
- resolving the option
- clicking the resolved option

If no matching option is found, a `NoSuchElementException` is raised.

---

## Option lookup semantics

Internally, Dropdown resolves options using:
- index-based access for integers
- Hyperion Element Query Language (EQL) for text and pattern matching

This allows expressive matching without exposing EQL as a required user concept.

---

## Selected value inspection

Dropdown exposes two complementary inspection APIs:
- **selected value** (semantic state)
- **selected option index** (structural position)

---

### `selected_value -> Optional[str]`

Returns the currently selected value as resolved by the dropdown.

Resolution behavior is controlled by `DropdownBySpec.value_attribute`:

- `"AUTO"` (default):
  - native `<select>` / `<input>` → resolve via `"value"` attribute
  - custom dropdowns → resolve visible text from label or trigger
- `"text"`:
  - always resolve visible text
- explicit attribute name:
  - resolve selected value from that DOM attribute

Returns `None` or an empty value if no selection is currently present.

---

### `selected_option_index -> Optional[int]`

Returns the index of the currently selected option, if resolvable.

The dropdown may be temporarily opened to ensure options are rendered
(e.g. for portal-based dropdowns).

Returns `None` if no matching option can be determined
(e.g. placeholder or unselected state).

---

## Verification and assertions

Dropdown follows Hyperion’s **verify vs assert** philosophy.

### Verification helpers (non-fatal)

- `verify_selected_value(expected)`
- `verify_has_option(option)`
- `verify_option_missing(option)`

These methods:
- do not fail the test
- return expectation objects
- are suitable for conditional logic and diagnostics

---

### Assertion helpers (fatal)

- `assert_selected_value(expected)`
- `assert_has_option(option)`
- `assert_option_missing(option)`

These methods:
- fail the test on mismatch
- provide rich diagnostic output

---

## Guarantees and non-goals

Hyperion guarantees:
- Dropdown resolves its structure exclusively from `DropdownBySpec`
- selected value resolution follows the declared or heuristic strategy
- options may be detached from the trigger hierarchy
- selection logic is deterministic and explicit
- open/close behavior is handled internally when required

Dropdown does **not**:
- guess where options are rendered
- assume a specific DOM hierarchy
- support searchable or async suggestion inputs
- implement arbitrary filtering logic

Controls that do not match the “trigger + flat options” model
should be implemented as different components.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: DropDown Specification](/docs/reference/public-api/dropdown-by-spec.md)  
→ Next: [Components: RadioGroup Specification](/docs/reference/public-api/radiogroup-by-spec.md)