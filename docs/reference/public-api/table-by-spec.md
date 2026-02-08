← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: RadioGroup](/docs/reference/public-api/radiogroup.md)  
→ Next: [Components: Table](/docs/reference/public-api/table.md)

---

# Component Spec: TableBySpec

`TableBySpec` defines the **declarative specification** for a table component.

It is a **data-only specification object** used inside Page Objects to describe:
- how table rows are enumerated
- how cells are located within each row
- optional header cell location
- optional slot policy rules that control how cells are materialized

Table modeling intentionally separates:
- **structure** (rows and cells locators)
- **behavior** (cell materialization via slot policy)

This enables reusable tables even when cell content is heterogeneous
(text cells, action panels, editable inputs, composite widgets).

---

## Public contract

### Constructor

```python
TableBySpec(
    root: LocatorTree,
    rows: LocatorTree,
    cells: LocatorTree,
    header_cells: Optional[LocatorTree] = None,
    slot_policy: Optional[SlotPolicyType] = None,
)
```

---

## Fields

### `root`

**Type:** `LocatorTree`  
**Required:** yes  

Defines the logical scope of the table.

The consuming component uses `root` as the component anchor and as the default
resolution scope for rows and header cells.

---

### `rows`

**Type:** `LocatorTree`  
**Required:** yes  

Defines how to locate the table rows.

Rows represent the currently rendered rows in the UI. This supports virtualized
tables implicitly: only rows present in the DOM are modeled.

---

### `cells`

**Type:** `LocatorTree`  
**Required:** yes  

Defines how to locate the table cells **within a row**.

This locator is purely structural: it identifies the root element of each cell.
Cell materialization (Element vs Widget) is controlled separately via `slot_policy`.

---

### `header_cells`

**Type:** `Optional[LocatorTree]`  
**Required:** no  

Defines how to locate the table header cells.

When provided, `header_cells` is expected to point **directly to header cell elements**
(e.g. `thead > td` or equivalent), rather than to a header wrapper.

Header cells may be used by the consuming component to derive column identity or
index mappings, but are not required for index-based tables.

---

### `slot_policy`

**Type:** `Optional[SlotPolicyType]`  
**Required:** no  

Defines an ordered list of slot policy rules controlling how cells are materialized.

Slot policies follow a policy-by-ordering model:
- rules are evaluated in order
- the **last matching rule wins**
- if no rule matches, a cell defaults to a plain `Element`

Rule kinds are inferred deterministically:
- `int` selector values represent index rules (supports negative indices, e.g. `-1`)
- reserved keywords represent predicate rules (e.g. `"ALL"`, `"LAST"`)
- other strings represent key-based rules (component-defined meaning)

EQL rules (Hyperion Element Query Language) must be explicitly declared and are never inferred.

---

## Intended usage

`TableBySpec` is used inside Page Object declarations via the `@table` decorator.

### Simple table (index-based)

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

---

### Table with header cells (optional)

```python
from hyperiontf import By, table, TableBySpec, WebPage


class UsersPage(WebPage):

    @table
    def users(self) -> TableBySpec:
        return TableBySpec(
            root=By.id("users"),
            header_cells=By.css("thead td"),
            rows=By.css("tbody tr"),
            cells=By.css("td"),
        )
```

---

### Mixed cell types via slot policy

```python
from hyperiontf import By, table, TableBySpec, SlotPolicyRule, WebPage


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
```

In this configuration:
- all cells are materialized as `InputCell`
- the last column is overridden to `ActionsCell`
- all matching is deterministic due to policy ordering

---

## Guarantees and non-goals

Hyperion guarantees:
- `TableBySpec` is treated as a declarative specification
- no element resolution occurs during Page Object construction
- the specification is preserved for use by the Table component

`TableBySpec` does **not**:
- scroll tables
- wait for virtualized rows to render
- validate table structure
- guarantee uniqueness of rows or cells
- implement selection or cell access APIs

Those responsibilities belong to the **Table component**.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: RadioGroup](/docs/reference/public-api/radiogroup.md)  
→ Next: [Components: Table](/docs/reference/public-api/table.md)