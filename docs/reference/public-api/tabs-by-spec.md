← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Carousel](/docs/reference/public-api/carousel.md)  
→ Next: [Components: Tabs](/docs/reference/public-api/tabs.md)

---

# Component Spec: TabsBySpec

`TabsBySpec` defines the declarative specification for the `Tabs` component.

It is a data-only object used inside Page Objects to describe:

- tab component scope (`root`)
- tab trigger collection (`tabs`)
- panel root collection (`panels`)
- optional tab label source (`tab_label`)
- panel lookup mode (`use_shared_panel`)
- optional slot materialization rules (`slot_policies`)

`TabsBySpec` describes structure only. Runtime behavior is implemented by `Tabs`.

---

## Public Contract

### Constructor

```python
TabsBySpec(
    root: LocatorTree,
    tabs: LocatorTree,
    panels: LocatorTree,
    use_shared_panel: bool = False,
    tab_label: Optional[LocatorTree] = None,
    slot_policies: Optional[SlotPolicyType] = None,
)
```

---

## Fields

### `root`

**Type:** `LocatorTree`  
**Required:** yes  

Logical root scope for the tabs component.

---

### `tabs`

**Type:** `LocatorTree`  
**Required:** yes  

Locator describing tab trigger items.

Each resolved tab is materialized as a `Button`-like trigger in `Tabs.tabs`.

---

### `panels`

**Type:** `LocatorTree`  
**Required:** yes  

Locator describing panel root nodes.

This supports both:

- multiple physical panels (1:1 tab-to-panel)
- a single shared panel holder (re-render model)

---

### `use_shared_panel`

**Type:** `bool`  
**Required:** no  
**Default:** `False`  

Controls active panel lookup mode:

- `False`: active panel is selected by index from `panels`
- `True`: physical root may stay `panels[0]`, while logical panel slot follows
  selected tab

Use `True` for re-render-in-place tab UIs.

---

### `tab_label`

**Type:** `Optional[LocatorTree]`  
**Required:** no  

Optional label locator relative to each tab trigger.

Use this when clickable tab root and visible text source are different nodes.

This also improves reliability for key-based slot policies using tab names.

---

### `slot_policies`

**Type:** `Optional[SlotPolicyType]`  
**Required:** no  

Ordered slot rules controlling panel materialization.

Supported selector forms:

- `int` index rule
- reserved predicate keywords (`"ALL"`, `"FIRST"`, `"LAST"`)
- key string rule (resolved via tab name -> index)
- explicit EQL rule (when kind is explicitly set)

Rule resolution follows policy-by-ordering (last matching rule wins).

---

## Intended Usage

`TabsBySpec` is intended for use with the `@tabs` decorator.

### 1:1 panel mapping

```python
TabsBySpec(
    root=By.id("tabs-1to1"),
    tabs=By.css(".tab-button"),
    panels=By.css(".tab-content"),
    tab_label=By.css(".tab-label"),
    slot_policies=[
        SlotPolicyRule(0, OverviewPanel),
        SlotPolicyRule(1, UsersPanel),
        SlotPolicyRule(2, SettingsPanel),
    ],
)
```

### Shared panel holder (mixed index + key rules)

```python
TabsBySpec(
    root=By.id("tabs-rerender"),
    tabs=By.css(".tab-button"),
    panels=By.css("#tabs-rerender-panel"),
    use_shared_panel=True,
    tab_label=By.css(".tab-label"),
    slot_policies=[
        SlotPolicyRule(0, HomePanel),
        SlotPolicyRule(1, ProfilePanel),
        SlotPolicyRule("Activity", ActivityPanel),
        SlotPolicyRule("Help", HelpPanel),
    ],
)
```

---

## Guarantees and Non-Goals

Hyperion guarantees:

- `TabsBySpec` is preserved as declarative input
- no eager element resolution at spec construction time
- mode selection is explicit via `use_shared_panel`
- slot policies are forwarded verbatim to runtime resolver

`TabsBySpec` does **not**:

- switch tabs
- resolve active panel eagerly
- validate DOM uniqueness or visibility
- perform assertions

Those responsibilities belong to the runtime `Tabs` component.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Carousel](/docs/reference/public-api/carousel.md)  
→ Next: [Components: Tabs](/docs/reference/public-api/tabs.md)
