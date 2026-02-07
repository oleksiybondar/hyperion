← [Back to Documentation Index](/docs/index.md)  
← Previous: [Component: Dropdown](/docs/how-to/dropdown.md)  
→ Next: [WebPage](/docs/reference/public-api/webpage.md)

---

# Table

This guide describes how to model **reusable Table widgets** in Hyperion using
a **declarative locator specification** and a **policy-by-ordering slot model**.

It focuses on **Page Object structure and locator design**, not on test logic
or Table interaction APIs.

Readers are expected to be familiar with Hyperion Page Objects, `By` locators,
and basic widget composition concepts.

> This document describes the intended usage pattern for reusable Table widgets.  
> The underlying implementation will follow this contract.

---

## What a Table represents

In Hyperion terms, a **Table** is:

- a logical container of **rows**
- where each row consists of **cells**
- and each cell may represent **different kinds of content**

Importantly:
- a table cell is **not always a simple element**
- cells may represent:
  - plain text
  - images
  - action panels
  - editable inputs
  - composite widgets

For this reason, Table modeling separates:
- **how cells are located** (structure)
- **how cells are materialized** (behavior)

---

## Core concepts

### Table
A **Table** is a complex widget declared on a Page Object using the `@table` decorator
and configured via a `TableBySpec`.

### Rows
Rows represent the repeatable, currently rendered table rows.
Virtualized tables are supported implicitly: only rows present in the DOM are modeled.

### Cells
Cells are located **structurally** within a row.
What a cell *becomes* (Element vs Widget) is decided separately via a policy.

### Header cells (optional)
Some tables provide header cells that can be used to derive column identity or index mappings.

In Hyperion, `header_cells` (when provided) should point **directly to header cell elements**
(e.g. `thead > td` or equivalent). It is optional and not required for index-based tables.

---

## Slot policies (brief introduction)

Some Table behaviors depend on **column position or identity**:
- “last column is actions”
- “second column is image”
- “all cells are inputs except the last one”

Hyperion models this using a **slot policy** (`slot_policy`).

A slot policy is:
- an **ordered list of rules**
- evaluated in order
- **last matching rule wins**

Each rule defines:
- **which slot it applies to** (by index, key, or fixed keyword)
- **what the slot should materialize as** (a target widget class)

If no rule matches, the cell defaults to a plain `Element`.

Notes:
- Rule kind inference is deterministic (`int` -> index; reserved keywords -> predicate; other strings -> key).
- EQL rules (Hyperion Element Query Language) must be explicitly declared and are never inferred automatically.

---

## Declaring a simple table (index-based)

### DOM shape

```html
<table id="users">
  <tr>
    <td>Alice</td>
    <td>Admin</td>
    <td><button>Edit</button></td>
  </tr>
</table>
```

### Modeling approach

- `root` scopes the table
- `rows` locates table rows
- `cells` locates all cells within a row
- no slot policy is required for simple tables

```python
from hyperiontf import By, table, TableBySpec, WebPage


class UsersPage(WebPage):

    @table
    def users(self) -> TableBySpec:
        return TableBySpec(
            root=By.id("users"),
            rows=By.css("tr"),
            cells=By.css("td"),
        )
```

In this case, all cells materialize as plain Elements.

---

## Mixed cell types using a slot policy

### Use case
- last column contains action buttons
- other columns are simple data cells

### Modeling approach

- keep `cells` purely structural
- use `slot_policy` to override cell materialization

```python
from hyperiontf import SlotPolicyRule, ActionsCell, TableBySpec, By


TableBySpec(
    root=By.id("users"),
    rows=By.css("tr"),
    cells=By.css("td"),
    slot_policy=[
        SlotPolicyRule(-1, ActionsCell),  # last column
    ],
)
```

Explanation:
- `-1` refers to the last cell in a row
- that cell materializes as `ActionsCell`
- all other cells remain plain Elements

---

## Editable tables (policy layering)

### Use case
- table is editable
- all cells are inputs
- last column is a save/apply button

### Modeling approach

```python
from hyperiontf import SlotPolicyRule, ActionsCell, InputCell, TableBySpec, By


TableBySpec(
    root=By.id("settings"),
    rows=By.css("tr"),
    cells=By.css("td"),
    slot_policy=[
        SlotPolicyRule("ALL", InputCell),
        SlotPolicyRule(-1, ActionsCell),
    ],
)
```

Because rules are evaluated in order:
- `"ALL"` applies first
- `-1` overrides it for the last column

This “last match wins” behavior is intentional and deterministic.

---

## Column keys and headers (optional)

In some tables, columns have stable identities (e.g. logical names).

When available, a Table may define `header_cells` to support **key-based slot rules**.
This is optional and not required for index-based tables.

Key-based selection is useful when:
- column order changes
- columns are conditionally hidden
- semantic identity matters more than position

Exact header mapping strategies are documented separately.

---

## Design guidelines

- Treat Table as a **structural + behavioral composition**
- Keep `cells` purely about *where* cells are
- Use `slot_policy` to decide *what* cells become
- Prefer index-based rules for simplicity
- Layer rules instead of writing complex conditions
- Do not assume all rows are rendered (virtualization)

---

## Summary

Table modeling in Hyperion is:

- declarative
- index-first
- policy-by-ordering
- extensible without subclassing

By separating structure from behavior, tables remain reusable even when
cells contain complex, heterogeneous content.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Component: Dropdown](/docs/how-to/dropdown.md)  
→ Next: [WebPage](/docs/reference/public-api/webpage.md)