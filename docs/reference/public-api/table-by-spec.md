← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: RadioGroup](/docs/reference/public-api/radiogroup.md)  
→ Next: [Components: Table](/docs/reference/public-api/table.md)

---

# Component Spec: TableBySpec

`TableBySpec` defines the **declarative specification** for a `Table` component.

It is a **data-only specification object** used inside Page Objects to describe:

- how table rows are enumerated  
- how cells are located within each row  
- optional header cell location  
- optional slot policy rules that control how cells are materialized  

`TableBySpec` describes **structure only**.  
All runtime behavior (row access, cell access, assertions, slot resolution, etc.)
is implemented by the `Table` component itself.

---

## Design Intent

Table modeling intentionally separates:

- **Structure** → row and cell locators  
- **Behavior** → runtime materialization via slot policy  
- **Interaction** → provided by returned cell wrappers (`Element` / `Widget`)  

This separation enables reusable tables even when cell content is heterogeneous
(text cells, action panels, editable inputs, composite widgets).

---

# Public Contract

## Constructor

{codeblock}python
TableBySpec(
    root: LocatorTree,
    rows: LocatorTree,
    cells: LocatorTree,
    header_cells: Optional[LocatorTree] = None,
    slot_policy: Optional[SlotPolicyType] = None,
)
{codeblock}

---

# Fields

## `root`

**Type:** `LocatorTree`  
**Required:** yes  

Defines the logical scope of the table.

The consuming `Table` component uses `root`:

- as the component anchor
- as the default resolution scope for rows
- as the default resolution scope for header cells

No element resolution occurs at spec construction time.

---

## `rows`

**Type:** `LocatorTree`  
**Required:** yes  

Defines how to locate table rows.

Rows represent the **currently rendered rows** in the UI.

Virtualized tables are implicitly supported:
only rows present in the DOM are modeled at runtime.

---

## `cells`

**Type:** `LocatorTree`  
**Required:** yes  

Defines how to locate table cells **within a row**.

This locator is purely structural:
it identifies the root element of each cell.

Cell materialization (plain `Element` vs specialized `Widget`)
is controlled separately via `slot_policy`.

---

## `header_cells`

**Type:** `Optional[LocatorTree]`  
**Required:** no  

Defines how to locate the table header cells.

When provided:

- `header_cells` must point **directly to header cell elements**
  (e.g. `thead > th` or equivalent)
- The `Table` component may derive column names from header text
- Key-based slot rules can resolve column names to indices
- Row-level key access (`row["Status"]`) becomes available

When omitted:

- Column-name-based access is unavailable
- Key-based slot rules may never match
- Index-based access remains fully supported

---

## `slot_policy`

**Type:** `Optional[SlotPolicyType]`  
**Required:** no  

Defines an ordered list of slot policy rules controlling
how cells are materialized.

Slot policies follow a **policy-by-ordering** model:

- Rules are evaluated in order
- The **last matching rule wins**
- If no rule matches, the cell defaults to a plain `Element`

Slot policies are evaluated at runtime by the `Table` component
via a `SlotRuleResolver`.

---

# Slot Rule Semantics

Rule kinds are inferred deterministically:

- `int` → index rule  
  - Supports negative indices (e.g. `-1` for last column)
- Reserved keywords → predicate rule  
  - e.g. `"ALL"`, `"FIRST"`, `"LAST"`
- Other strings → key-based rule  
  - Resolved via header name → index mapping
- Explicit `kind=SlotRuleKind.EQL` → EQL rule  
  - Expression evaluated against the cell element

Key-based rules only match when:

- `header_cells` is configured, and
- the column name can be resolved to an index

If header resolution fails, the rule does not match.

---

# Intended Usage

`TableBySpec` is used inside Page Object declarations
via the `@table` decorator.

---

## Simple table (index-based)

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

## Table with header cells

{codeblock}python
from hyperiontf import By, table, TableBySpec, WebPage

class UsersPage(WebPage):

    @table
    def users(self) -> TableBySpec:
        return TableBySpec(
            root=By.id("users"),
            header_cells=By.css("thead th"),
            rows=By.css("tbody tr"),
            cells=By.css("td"),
        )
{codeblock}

This enables:

- `row["ColumnName"]` access
- Key-based slot rules

---

## Mixed cell types via slot policy

{codeblock}python
from hyperiontf import By, table, TableBySpec, SlotPolicyRule, WebPage
from myproject.widgets import InputCell, ActionsCell

class UsersPage(WebPage):

    @table
    def users(self) -> TableBySpec:
        return TableBySpec(
            root=By.id("users"),
            rows=By.css("tr"),
            cells=By.css("td"),
            slot_policy=[
                SlotPolicyRule("ALL", InputCell),
                SlotPolicyRule(-1, ActionsCell),
            ],
        )
{codeblock}

In this configuration:

- All cells materialize as `InputCell`
- The last column overrides to `ActionsCell`
- Matching is deterministic due to rule ordering

---

# Runtime Guarantees

Hyperion guarantees:

- `TableBySpec` is treated as a declarative specification
- No element resolution occurs during Page Object construction
- Slot policy evaluation occurs lazily at runtime
- Cell wrapper instantiation is cached after first resolution

---

# Non-Goals

`TableBySpec` does **not**:

- Scroll tables
- Trigger rendering of virtualized rows
- Validate DOM structure
- Guarantee uniqueness of rows or cells
- Provide row selection or filtering APIs
- Perform any assertions

Those responsibilities belong to the **Table component**.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: RadioGroup](/docs/reference/public-api/radiogroup.md)  
→ Next: [Components: Table](/docs/reference/public-api/table.md)