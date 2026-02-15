← [Back to Documentation Index](/docs/index.md)  
← Previous: [Component: Carousel](/docs/how-to/carousel.md)  
→ Next: [WebPage](/docs/reference/public-api/webpage.md)

---

# Tabs

This guide explains how to model reusable **Tabs** components in Hyperion using
`TabsBySpec` and the `@tabs` decorator.

It focuses on **component design and Page Object modeling**, not on test design.

---

## Core Model

A `Tabs` component is defined by five concepts:

- `root`: logical scope of the tabs component
- `tabs`: locator for tab trigger items
- `panels`: locator for panel root(s)
- `tab_label` (optional): label source for tab identity/text
- `slot_policies` (optional): mapping from logical slot to concrete panel widget class

`Tabs.activate(...)` accepts:

- `int` (index)
- `str` (exact name)
- `re.Pattern` (pattern selector)

---

## Two Runtime Modes

### Mode A: One tab -> one panel (`use_shared_panel=False`)

Use this when each tab owns its own physical panel node.

- `panels` resolves multiple items
- active panel is selected by active tab index
- slot policies are typically index-based (or key-based if names are stable)

### Mode B: Many tabs -> one panel holder (`use_shared_panel=True`)

Use this when content is re-rendered inside a single panel root.

- `panels` usually resolves only one item (`panels[0]`)
- active content still maps to a logical tab slot
- slot policies remain applicable and are resolved by selected tab

This is an intended and separate modeling branch.

---

## Modeling Pattern

Declare tabs as typed component specs on Page Objects.

```python
from hyperiontf import By, SlotPolicyRule, TabsBySpec, WebPage
from hyperiontf.ui.components.decorators.page_object_helpers import tabs


class TabsPage(WebPage):

    @tabs
    def tabs_1to1(self) -> TabsBySpec:
        return TabsBySpec(
            root=By.id("tabs-1to1"),
            tabs=By.css("#tabs-1to1-buttons .tab-button"),
            panels=By.css("#tabs-1to1-contents .tab-content"),
            tab_label=By.css(".tab-label"),
            slot_policies=[
                SlotPolicyRule(0, OverviewPanel),
                SlotPolicyRule(1, UsersPanel),
                SlotPolicyRule(2, SettingsPanel),
            ],
        )

    @tabs
    def tabs_rerender(self) -> TabsBySpec:
        return TabsBySpec(
            root=By.id("tabs-rerender"),
            tabs=By.css("#tabs-rerender-buttons .tab-button"),
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

## Slot Policy Design

Slot policies define how panel slots are materialized into widget classes.

### Index rules

Use for deterministic, position-based mapping:

- `SlotPolicyRule(0, HomePanel)`
- `SlotPolicyRule(1, ProfilePanel)`

### Key rules

Use when tab label semantics are stable and meaningful:

- `SlotPolicyRule("Activity", ActivityPanel)`
- `SlotPolicyRule("Help", HelpPanel)`

For key rules, `tab_label` should be configured so tab names resolve consistently.

---

## Panel Widget Modeling

Use one widget class per logical panel type.

Recommended shape:

- keep one widget per file
- expose at least one unique element for that panel
- keep locators local to panel root

Example:

```python
from hyperiontf import By, Widget, element


class ProfilePanel(Widget):
    @element
    def title(self):
        return By.css("strong")

    @element
    def profile_name(self):
        return By.id("profile-name")
```

This keeps slot materialization explicit and avoids ambiguous panel identity.

---

## Selection Semantics

Tabs selection is expression-driven:

```python
tabs.activate(2)                      # index
tabs.activate("Users")               # exact label
tabs.activate(re.compile(r"Over.*"))  # pattern
```

Use the selector form that best expresses intent in your domain model.

---

## Memoization Notes

Tabs expose logical panel objects. Behavior differs by mode:

- Static mode (`use_shared_panel=False`): panel objects map to stable physical panel slots.
- Shared mode (`use_shared_panel=True`): one physical panel root is reused, while logical slot resolution follows selected tab.

Model your Page Object API around logical slot identity, not raw DOM count.

---

## Common Modeling Mistakes

- Treating shared-panel mode as “no slot policy needed”.
- Mixing unrelated panel locators into one widget class.
- Omitting `tab_label` while relying on key-based rules.
- Modeling panel internals as generic elements when semantic widgets are clearer.

---

## Summary

`TabsBySpec` supports both static multi-panel tabs and shared re-rendered tabs.
Use slot policies to map logical tab slots to explicit widget classes, and keep
panel widgets focused and unique.

The result is a stable, declarative tabs model that stays consistent even when
DOM rendering strategy changes.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Component: Carousel](/docs/how-to/carousel.md)  
→ Next: [WebPage](/docs/reference/public-api/webpage.md)

