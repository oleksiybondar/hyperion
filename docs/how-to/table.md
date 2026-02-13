← [Back to Documentation Index](/docs/index.md)  
← Previous: [Component: Dropdown](/docs/how-to/dropdown.md)  
→ Next: [Component: Carousel](/docs/how-to/carousel.md)

---

# Table

This guide describes how to model **reusable Table widgets** in Hyperion using
a **declarative locator specification** (`TableBySpec`) and a
**policy-by-ordering slot model**.

It focuses on **Page Object structure and locator design**, not on test logic
or the runtime Table interaction API.

Readers are expected to be familiar with:

- Hyperion Page Objects
- `By` locators
- Component decorators
- Basic widget composition

> The runtime behavior described here is implemented by the `Table` component.

---

## What a Table Represents

In Hyperion terms, a **Table** is:

- A logical container of **rows**
- Where each row consists of **cells**
- And each cell may represent **different kinds of content**

Importantly:

- A table cell is **not necessarily a simple element**
- Cells may represent:
  - Plain text
  - Images
  - Action panels
  - Editable inputs
  - Composite widgets

For this reason, Table modeling separates:

- **Structure** → how rows and cells are located
- **Behavior** → how cells are materialized (Element vs Widget)

This separation keeps Page Objects declarative and reusable.

---

# Core Concepts

## Table

A **Table** is declared on a Page Object using the `@table` decorator
and configured via a `TableBySpec`.

The decorator converts a specification into a lazily constructed
`Table` component.

---

## Rows

Rows represent the repeatable, currently rendered table rows.

Important:

- Only rows present in the DOM are modeled.
- Virtualized tables are supported implicitly.
- No automatic scrolling or virtualization handling is performed.

---

## Cells

Cells are located **structurally** within each row using the `cells` locator
defined in `TableBySpec`.

The `cells` locator:

- Must identify the **root element of each cell**
- Should not contain behavior assumptions
- Is purely structural

What a cell *becomes* at runtime (plain `Element` vs custom `Widget`)
is determined separately via `slot_policies`.

Cells are:

- Materialized lazily
- Resolved on first access
- Cached per row

---

## Header Cells (Optional)

Some tables expose header cells that define column identity.

When provided, `header_cells` should point **directly to header cell elements**
(e.g. `thead > th`).

When configured, headers enable:

- Key-based cell access (`row["Status"]`)
- Key-based slot policy rules
- Column name assertions at runtime

When omitted:

- Only index-based access is available
- Key-based slot rules may never match

Headers are optional and not required for index-based tables.

---

# Slot Policies

Some Table behaviors depend on **column position or identity**, for example:

- “Last column is actions”
- “Second column is image”
- “All cells are inputs except the last one”

Hyperion models this using a **slot policy** (`slot_policies`).

A slot policy is:

- An **ordered list of rules**
- Evaluated in order
- **Last matching rule wins**

Each rule defines:

- Which slot it applies to  
  (index, predicate keyword, key, or explicit EQL expression)
- What wrapper class the slot should materialize as

If no rule matches, the cell defaults to a plain `Element`.

---

## Rule Types

Rule kind inference is deterministic:

- `int` → index rule  
  - Supports negative indices (`-1` last, `-2` second-to-last)
- Reserved keywords → predicate rule  
  - `"ALL"`, `"FIRST"`, `"LAST"`
- Other strings → key-based rule  
  - Resolved via header name → column index mapping
- Explicit `kind=SlotRuleKind.EQL` → EQL rule  
  - Evaluated against the cell element

Key-based rules require `header_cells` to be configured.

---

# Declaring a Simple Table (Index-Based)

## DOM Shape

{codeblock}html
<table id="users">
  <tr>
    <td>Alice</td>
    <td>Admin</td>
    <td><button>Edit</button></td>
  </tr>
</table>
{codeblock}

## Modeling Approach

- `root` scopes the table
- `rows` locates table rows
- `cells` locates cells within a row
- No slot policy is required

{codeblock}python
from hyperiontf import By, table, TableBySpec, WebPage

class UsersPage(WebPage):

    @table
    def users(self) -> TableBySpec:
        return TableBySpec(
            root=By.id("users"),
            rows=By.css("tr"),
            cells=By.css("td"),
        )
{codeblock}

All cells materialize as plain `Element` instances.

---

# Mixed Cell Types Using Slot Policy

## Use Case

- Last column contains action buttons
- Other columns are simple data cells

## Modeling Approach

Keep `cells` purely structural and override materialization via `slot_policies`.

{codeblock}python
from hyperiontf import SlotPolicyRule, ActionsCell, TableBySpec, By

TableBySpec(
    root=By.id("users"),
    rows=By.css("tr"),
    cells=By.css("td"),
    slot_policies=[
        SlotPolicyRule(-1, ActionsCell),
    ],
)
{codeblock}

Explanation:

- `-1` refers to the last column
- That cell materializes as `ActionsCell`
- All other cells remain plain `Element`

---

# Editable Tables (Policy Layering)

## Use Case

- All cells are editable inputs
- Last column contains action buttons

## Modeling Approach

{codeblock}python
from hyperiontf import SlotPolicyRule, ActionsCell, InputCell, TableBySpec, By

TableBySpec(
    root=By.id("settings"),
    rows=By.css("tr"),
    cells=By.css("td"),
    slot_policies=[
        SlotPolicyRule("ALL", InputCell),
        SlotPolicyRule(-1, ActionsCell),
    ],
)
{codeblock}

Explanation:

- `"ALL"` applies to every cell
- `-1` overrides for the last column
- Rule ordering guarantees deterministic resolution

---

# Column Keys and Headers

Key-based rules are useful when:

- Column order changes
- Columns are conditionally hidden
- Semantic identity matters more than index

When `header_cells` is defined:

- Header text is used to derive column names
- Key-based slot rules can match by name
- Rows support key-based access (`row["Status"]`)

If headers are not configured:

- Key-based rules may never match
- Only index-based rules are reliable

---

# Accessing Cells

Cells can be accessed using index or key:

{codeblock}python
row = page.users[0]

row[0]        # first column
row[-1]       # last column
row["Status"] # header-based access
{codeblock}

The returned object type depends on slot policy resolution.

---

# Design Guidelines

- Treat Table as a **structural + behavioral composition**
- Keep `cells` purely about *where* cells are
- Use `slot_policies` to decide *what* cells become
- Prefer index-based rules for simplicity
- Layer simple rules instead of complex logic
- Do not assume all rows are rendered
- Do not rely on wrapper type before accessing the cell

---

# Summary

Table modeling in Hyperion is:

- Declarative
- Index-first
- Policy-by-ordering
- Extensible via custom cell widgets
- Lazy in resolution
- Deterministic in materialization

By separating structure from behavior, tables remain reusable even when
cells contain complex, heterogeneous content.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Component: Dropdown](/docs/how-to/dropdown.md)  
→ Next: [Component: Carousel](/docs/how-to/carousel.md)
