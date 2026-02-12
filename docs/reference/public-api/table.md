← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Table Specification](/docs/reference/public-api/table-by-spec.md)  
→ Next: [Components: Carousel Specification](/docs/reference/public-api/carousel-by-spec.md)

---

# Component API: Table

This document describes the **runtime API** exposed by the `Table` component.

Unlike `TableBySpec`, which is declarative and structure-focused, this page
documents how a `Table` behaves when used in tests.

A Table exposes three runtime actors:

- **Table** — collection of rows  
- **Row** — collection of cells  
- **Cell** — resolved wrapper (`Element` or slot-resolved `Widget`)  

The API intentionally mirrors Python collection semantics while supporting
heterogeneous cell types through slot resolution.

---

## Conceptual Model

A `Table` behaves like a 2-dimensional collection:

```python
table[row_index][column_index]
table[row_index]["ColumnName"]
```

The returned object is a **Cell**, which may be:

- a plain `Element`
- or a specialized widget resolved by slot policy

The exact runtime type depends on the configured `slot_policy`.

Only **currently rendered rows and cells** are modeled. Virtualized tables
are supported implicitly: only present DOM/UI nodes are represented.

---

# Table API

The `Table` object represents the collection of currently rendered rows.

---

## Collection Behavior

### `len(table) -> int`

Returns the number of currently rendered rows.

```python
assert len(page.users) == 5
```

---

### `table[index] -> Row`

Returns the row at the given index.

- Supports negative indices.
- Raises `IndexError` if out of bounds.

```python
row = page.users[0]
last = page.users[-1]
```

---

### `for row in table`

Iterates over rows.

```python
for row in page.users:
    row[0].assert_text("Alice")
```

---

## Assertions & Verification

Table provides structural expectation helpers.  
All assertions are **fail-fast**.  
All verification methods return a bool-compatible `ExpectationResult`.

---

### `table.assert_has_rows(min_rows: int = 1)`

Asserts the table has **at least** `min_rows` rows.

- Raises on failure.
- Returns `ExpectationResult` on success.

---

### `table.verify_has_rows(min_rows: int = 1)`

Verifies the table has **at least** `min_rows` rows.

- Never raises.
- Returns `ExpectationResult`.

---

### `table.assert_row_count(expected: int)`

Asserts the table row count equals `expected`.

---

### `table.verify_row_count(expected: int)`

Verifies the table row count equals `expected`.

---

### `table.assert_columns_names(expected_names: list[str])`

Asserts that derived header column names exactly match `expected_names`.

- Order-sensitive comparison.
- Requires `header_cells` to be configured in `TableBySpec`.
- Raises `AssertionError` if headers are not configured.

---

### `table.verity_columns_names(expected_names: list[str])`

Verifies that header column names match `expected_names`.

Returns:

- `False` if headers are not configured  
- otherwise an `ExpectationResult`

Note: method name reflects current implementation.

---

### `table.assert_table_normalized() -> bool`

Checks that the table is **normalized**.

A table is considered normalized when:

- each rendered row contains the same number of cells
- expected cell count is derived from:
  - header cell count (if headers configured), or
  - the first row's cell count

Returns `True` when normalized.

---

### `table.verity_table_normalized() -> bool`

Non-throwing normalization check.

Returns `True` if all rows match expected cell count, otherwise `False`.

---

# Row API

A `Row` represents a collection of cells.

It behaves like a sequence and supports both index and key access.

---

## Index Access

### `row[column_index] -> Cell`

Returns cell at the given position.

- Supports negative indices.

```python
row = page.users[0]
cell = row[-1]
```

---

## Key Access (Requires Headers)

### `row[column_name] -> Cell`

Returns cell resolved by header name.

```python
row = page.users[0]
status = row["Status"]
```

Behavior depends on table configuration:

- When headers are configured, column names are resolved to indices.
- When headers are not configured, string indexing falls back to base
  collection behavior.

---

## Iteration

### `for cell in row`

Iterates over all cells in the row.

---

## Length

### `len(row) -> int`

Returns the number of currently rendered cells.

---

## Row-Level Assertions

### `row.assert_has_cells(min_cells: int = 1)`

Asserts the row contains at least `min_cells` cells.

---

### `row.verify_has_cells(min_cells: int = 1)`

Verifies the row contains at least `min_cells` cells.

---

### `row.assert_row_cells(expected: int)`

Asserts the row contains exactly `expected` cells.

---

### `row.verify_row_cells(expected: int)`

Verifies the row contains exactly `expected` cells.

---

# Cell API

A Cell is **not a fixed class**.

At runtime it is either:

- `Element`
- or a slot-resolved `Widget` (e.g. `ActionsCell`, `InputCell`, `IconCell`, etc.)

The Table component does not expose a separate base Cell class.
Instead, it returns whichever wrapper the slot policy resolves.

---

## Guaranteed Behavior

Every Cell supports the full **Element API**:

```python
cell.assert_text("Alice")
cell.click()
cell.get_text()
cell.assert_visible()
```

---

## Slot-Resolved Behavior

If a slot policy matches, the returned object exposes its widget-specific API:

```python
row["Actions"].buttons[0].click()
row["Status"].select("Active")
row["Icon"].icon.assert_visible()
```

---

## Type Expectations

Users should not rely on concrete types unless necessary.

Recommended:

```python
row["Actions"].buttons[0].click()
```

Allowed but optional:

```python
assert isinstance(row[-1], ActionsCell)
```

---

## Resolution Model

Cell type resolution follows this process:

1. Structural cell element located  
2. Slot policy evaluated  
3. Final wrapper class selected  
4. Wrapper instance cached  

Subsequent access returns the same instance.

Resolution is deterministic and policy-by-ordering (last matching rule wins).

---

## Failure Behavior

- Index out of range → `IndexError`
- Missing headers for name-based column assertion → `AssertionError`
- Failed assertions → `FailedExpectationException`
- Verification failures → return `ExpectationResult` (bool-compatible)
- Normalization verification returns `bool`

---

## Example Usage

```python
table = page.users

table.assert_row_count(3)

row = table[0]
row[0].assert_text("Alice")
row["Status"].select("Active")
row[-1].buttons[1].click()
```

---

## Design Intent

The Table API provides:

- Pythonic collection semantics  
- Deterministic slot resolution  
- Heterogeneous cell behavior  
- Lazy materialization  
- Structural validation helpers  

This allows complex tables to behave naturally in tests while remaining
declarative in Page Object definitions.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Components: Table Specification](/docs/reference/public-api/table-by-spec.md)  
→ Next: [Components: Carousel Specification](/docs/reference/public-api/carousel-by-spec.md)