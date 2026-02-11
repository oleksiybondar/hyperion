← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: RadioGroup Specification](/docs/reference/public-api/radiogeoup-by-spec.md)  
→ Next: [Components: Table Specification](/docs/reference/public-api/table-by-spec.md)

---

# Component: Radiogroup

`Radiogroup` is a reusable component representing a logical group of
mutually exclusive options.

It is declared on a Page Object using the `@radiogroup` decorator and
configured via a `RadioGroupBySpec`.

The component provides:

- selection by index, text, or pattern
- deterministic checked-state evaluation
- introspection helpers (selected item, index, text)
- assertion helpers for test verification

---

## Declaration

A Radiogroup is declared by returning a `RadioGroupBySpec`
from a Page Object property decorated with `@radiogroup`.

{codeblock}python
from hyperiontf import By, radiogroup, RadioGroupBySpec, WebPage


class SettingsPage(WebPage):

    @radiogroup
    def notifications(self) -> RadioGroupBySpec:
        return RadioGroupBySpec(
            root=By.id("notifications"),
            items=By.css(".radio-item"),
            input=By.css("input[type='radio']"),
            label=By.css("label"),
        )
{codeblock}

---

## Public API

### `radio_items`

{codeblock}python
@property
def radio_items(self) -> Collection[RadioItem]
{codeblock}

Returns the collection of `RadioItem` instances defined by
`RadioGroupBySpec.items`.

Items may be accessed:

- by index (`radio_items[0]`)
- by EQL selector (`radio_items["attribute:checked == \"true\""]`)

---

### `checked_expression`

{codeblock}python
@property
def checked_expression(self) -> str
{codeblock}

Returns the EQL expression used to identify the selected item.

- If defined in `RadioGroupBySpec`, that expression is returned.
- Otherwise defaults to:

{codeblock}text
attribute:checked == "true"
{codeblock}

Note: Boolean coercion is not currently supported in EQL.  
Boolean-like attributes must be compared as strings.

---

## Selection

### `select`

{codeblock}python
def select(self, item: Union[int, str, re.Pattern]) -> None
{codeblock}

Select a radio option.

Accepted selector types:

- `int` — index in the collection
- `str` — semantic text match
- `re.Pattern` — regex match

Raises:

- `NoSuchElementException` if a text/pattern match fails.

---

## Introspection

### `selected_item`

{codeblock}python
@property
def selected_item(self) -> Optional[RadioItem]
{codeblock}

Returns the currently selected `RadioItem`, or `None` if no
item matches `checked_expression`.

---

### `selected_item_text`

{codeblock}python
@property
def selected_item_text(self) -> Optional[str]
{codeblock}

Returns the text/identity of the selected item.

Text resolution depends on the component spec:

- If `label` is defined → label text
- Otherwise → item root text

---

### `selected_item_index`

{codeblock}python
@property
def selected_item_index(self) -> Optional[int]
{codeblock}

Returns the index of the selected item.

The index reflects the position of the item in the collection.
It remains stable while that slot exists in the resolved collection.

Returns `None` if no item is selected.

---

## Assertions

All assertion methods fail the test when the condition is not met.

---

### `assert_selected_value`

{codeblock}python
def assert_selected_value(self, expected: Union[str, re.Pattern])
{codeblock}

Assert that the selected item's text matches the expected value.

---

### `assert_selected_index`

{codeblock}python
def assert_selected_index(self, expected: int)
{codeblock}

Assert that the selected item's index matches the expected index.

---

### `assert_radio_state`

{codeblock}python
def assert_radio_state(
    self,
    selected: Optional[Union[int, str, re.Pattern]] = None
)
{codeblock}

Assert high-level RadioGroup invariants.

If `selected` is provided:

- `int` → asserts selected index
- `str` / `re.Pattern` → asserts selected value

Additionally asserts that at most one item is selected.

---

### `assert_none_selected`

{codeblock}python
def assert_none_selected(self)
{codeblock}

Assert that no item is currently selected.

Note: This is only meaningful for custom radio implementations
that allow a “no selection” state.

---

### `assert_only_one_selected`

{codeblock}python
def assert_only_one_selected(self)
{codeblock}

Assert that exactly one item is selected.

---

### `assert_at_most_one_selected`

{codeblock}python
def assert_at_most_one_selected(self)
{codeblock}

Assert that zero or one items are selected.

This enforces the mutual-exclusion invariant of a radio group.

---

### `assert_has_item`

{codeblock}python
def assert_has_item(self, item: Union[str, re.Pattern])
{codeblock}

Assert that an item matching the given text or pattern exists.

---

### `assert_item_missing`

{codeblock}python
def assert_item_missing(self, item: Union[str, re.Pattern])
{codeblock}

Assert that an item matching the given text or pattern does not exist.

---

## Resolution Guarantees

Hyperion guarantees:

- Selection and checked-state evaluation follow the deterministic
  resolution order defined by `RadioGroupBySpec`.
- `checked_expression` is evaluated against:
  - the resolved `input` node if defined
  - otherwise the item root node
- Only one selected item is expected in well-formed native radio groups.

The component does not:

- Validate DOM structure beyond the specification
- Enforce business rules beyond mutual exclusion

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: RadioGroup Specification](/docs/reference/public-api/radiogeoup-by-spec.md)  
→ Next: [Components: Table Specification](/docs/reference/public-api/table-by-spec.md)