← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Tabs Specification](/docs/reference/public-api/tabs-by-spec.md)  
→ Next: [Behavior Contracts: Locator Resolution Order](/docs/reference/behavior-contracts/locator-resolution.md)

---

# Component: Tabs

`Tabs` is a reusable navigation component that models tab triggers and tab-bound
content panels.

It supports two structural modes:

- multi-panel mode (`use_shared_panel=False`): one logical tab maps to one panel node
- shared-panel mode (`use_shared_panel=True`): one physical panel node is reused,
  while logical content changes by active tab

`Tabs` is specification-driven and consumes `TabsBySpec`.

---

## Declaration

A Tabs component is declared in a Page Object via `@tabs` and `TabsBySpec`.

```python
from hyperiontf import By, tabs, TabsBySpec, WebPage


class SettingsPage(WebPage):

    @tabs
    def account_tabs(self) -> TabsBySpec:
        return TabsBySpec(
            root=By.id("account-tabs"),
            tabs=By.css(".tab-button"),
            panels=By.css(".tab-panel"),
            tab_label=By.css(".tab-label"),
        )
```

---

## Public Contract

### `tabs -> Components[Button]`

Returns the tabs trigger collection as `Button` components.

Identity/text resolution for each tab trigger uses `tab_label` when configured.

---

### `panels -> Slots`

Returns the panel collection with slot-policy materialization.

Each slot may be returned as a plain `Element` or a specialized widget/component,
depending on `slot_policies`.

---

### `panel`

Returns the currently active panel.

Resolution differs by mode:

- `use_shared_panel=False`: returns `panels[selected_tab_index]`
- `use_shared_panel=True`: starts from `panels[0]` and resolves wrapper class
  by current selected tab index (logical slot)

---

### `activate(tab_name: Union[str, int, re.Pattern])`

Activates a tab by:

- index (`int`)
- exact tab name (`str`)
- regex/pattern (`re.Pattern`)

Behavior:

- resolves tab trigger and clicks it
- updates `selected_tab_index`
- in shared-panel mode, refreshes tabs/panels collections after click

Raises:

- `NoSuchElementException` if no matching tab is found

---

### `selected_tab_index -> int`

Current selected tab index tracked by the component.

Initial value is `0`.

---

### `selected_tab_name -> str`

Returns the selected tab name resolved from cached `tabs_names`.

---

### `tabs_names -> List[str]`

Lazy-cached list of tab names resolved from tab triggers.

Cache is reset by `force_refresh()`.

---

### `force_refresh()`

Resets internal state and refreshes tabs/panels collections.

State reset:

- cached tab names
- selected tab index (back to `0`)

---

## Selection Semantics

Text and regex selection are resolved through EQL selector generation.

Examples:

```python
tabs.activate(2)
tabs.activate("Users")
tabs.activate(re.compile(r"Over.*"))
```

---

## Slot Materialization Semantics

Tabs uses `SlotRuleResolver` with rule ordering semantics (last matching rule wins).

Key-based slot policies are supported through tab name -> index resolution.

This applies to both modes, including shared-panel mode where only one physical
panel node may exist.

---

## Assertions and Verification

`Tabs` provides both non-fatal verification and fatal assertion helpers:

- `verify_has_tab(tab)`
- `verify_itab_missing(tab)`  (legacy method name)
- `assert_has_tab(tab)`
- `assert_tab_missing(tab)`

Verification helpers return expectation objects for decision flow.
Assertion helpers fail on mismatch.

---

## Guarantees and Non-Goals

Hyperion guarantees:

- spec-driven tab/panel resolution
- deterministic slot policy evaluation
- explicit selector-based activation (index/text/pattern)
- shared-panel logical slot resolution by selected tab

`Tabs` does **not**:

- infer tab structure heuristically
- auto-create slot policies
- model non-tab navigation patterns

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Tabs Specification](/docs/reference/public-api/tabs-by-spec.md)  
→ Next: [Behavior Contracts: Locator Resolution Order](/docs/reference/behavior-contracts/locator-resolution.md)
