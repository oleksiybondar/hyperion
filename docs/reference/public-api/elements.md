← [Back to Documentation Index](/docs/index.md)  
← Previous: [Element](/docs/reference/public-api/element.md)  
→ Next: [By](/docs/reference/public-api/by.md)

---

# Elements

`Elements` represents a **collection of `Element` objects** resolved from a single locator.

Use it when a locator matches **multiple nodes** (rows, items, cards, chips, etc.).

Key characteristics:
- indexing and iteration yield regular `Element` instances (full `Element` API)
- collection-level waits operate on **count and presence**
- supports **EQL-powered selection** via string indexing

> `Elements` is a collection of leaves — it is not a structural container like `Widget`.

---

## Conceptual role

| Aspect | Meaning |
|---|---|
| Structural container | No (collection of leaves) |
| Hierarchical | Yes (belongs to a parent container) |
| Item type | `Element` |
| Context boundary | No (inherits context from parent container) |
| Stability model | Retries + recovery are applied automatically |

---

## Declaring Elements in Page Objects

`Elements` is usually declared via `@elements` on a `WebPage`, `Widget`, `IFrame`, or `WebView`.

```python
from hyperiontf import WebPage, elements, By


class ResultsPage(WebPage):

    @elements
    def rows(self):
        return By.css(".result-row")
```

---

## Collection behavior

### __len__() -> int

`len(elements)` returns the number of currently resolved items.

```python
def test_results_present(results_page):
    results_page.rows.wait_until_found()
    assert len(results_page.rows) >= 1
```

### __iter__() -> Iterator[Element]

Iterating yields `Element` items.

```python
def test_all_rows_visible(results_page):
    results_page.rows.wait_until_found()

    for row in results_page.rows:
        row.assert_visible()
```

### __getitem__(index: int) -> Element

Indexing yields the item at the given position.

- supports negative indices (`-1` is the last item)

```python
def test_first_row_clickable(results_page):
    results_page.rows.wait_until_found()

    results_page.rows[0].click()
    results_page.rows[-1].scroll_into_view()

    results_page.status_banner.assert_visible()
```

---

## Presence

### is_present: bool

`True` if at least one item is present, otherwise `False`.

This answers:

- “is there at least one match right now?”

It does **not** wait.  
Use waits when you need synchronization.

---

## Cache and refresh behavior

`Elements` caches resolved items and may refresh internally when the underlying result set changes.

### force_refresh() -> None

Clears the internal cache and re-finds the collection immediately.

Use `force_refresh()` after a UI change when you want to re-evaluate matches right away (for example, after applying filters).

---

## Collection waits

All waits are **interactive** (polling + retries), not passive sleeping.

### wait_until_found() -> None

Waits until at least one item exists.

### wait_until_missing() -> None

Waits until no items exist.

### wait_until_items_count(expected_count: int) -> None

Waits until item count equals the expected count.

- `expected_count`: expected number of items

### wait_until_items_decrease() -> None

Waits until the item count decreases compared to the previous observation.

### wait_until_items_increase() -> None

Waits until the item count increases compared to the previous observation.

### wait_until_items_change() -> None

Waits until the item count changes (increase or decrease) compared to the previous observation.

#### Example: wait for results to load

```python
def test_results_load(results_page):
    results_page.rows.wait_until_found()
    assert len(results_page.rows) > 0
```

#### Example: wait for list to refresh after filtering

```python
from hyperiontf import WebPage, element, elements, By


class ResultsPage(WebPage):

    @element
    def filter_button(self):
        return By.id("filter")

    @elements
    def rows(self):
        return By.css(".result-row")


def test_filter_refresh(results_page: ResultsPage):
    results_page.rows.wait_until_found()
    before = len(results_page.rows)

    results_page.filter_button.click()
    results_page.rows.wait_until_items_change()

    after = len(results_page.rows)

    # Explicit outcome checks
    assert after != before
    assert after >= 1
    results_page.rows[0].assert_visible()
```

---

## EQL selection on collections

`Elements` supports **EQL-powered lookup** via string indexing:

- `elements["<EQL query>"] -> Element | None`
- the query is evaluated against each item
- the first match is returned
- if nothing matches, `None` is returned

This enables semantic selection (“the row with title X”) instead of brittle index-based selection.

### Supported Element attributes in EQL

When evaluating an EQL expression against an `Element`, Hyperion resolves:

| EQL attribute | Maps to |
|---|---|
| `text` | `Element.get_text()` |
| `style.<name>` | `Element.get_style(<name>)` |
| `<attribute_name>` | `Element.get_attribute(<attribute_name>)` |

> EQL syntax itself (operators, grouping, etc.) is defined by the EQL language. This page documents the integration points and supported attributes.

### __getitem__(query: str) -> Element | None

Select the first matching element using an EQL query.

#### Example: select by visible text

```python
def test_select_row_by_text(results_page):
    results_page.rows.wait_until_found()

    row = results_page.rows['text == "Coffee Mug"']
    assert row is not None

    row.click()
    results_page.toast.assert_visible()
```

#### Example: select by attribute (stable test id)

```python
def test_select_row_by_test_id(results_page):
    results_page.rows.wait_until_found()

    item = results_page.rows['data_test_id == "result-42"']
    assert item is not None

    item.assert_visible()
```

#### Example: select by computed style

```python
def test_select_active_row(results_page):
    results_page.rows.wait_until_found()

    active = results_page.rows['style.color == "rgba(0, 0, 0, 1)"']
    assert active is not None

    active.click()
    results_page.details_panel.assert_visible()
```

### Guidance for EQL usage

- Prefer EQL when list order is unstable and selection should be meaning-based.
- Handle “not found” explicitly:
  - assert a match exists (`assert match is not None`)
  - or branch intentionally (`if match:`), then still end with explicit assertions.

```python
def test_select_role_if_present(results_page):
    results_page.rows.wait_until_found()

    target = results_page.rows['text == "Admin"']

    if target:
        target.click()
        results_page.toast.assert_text("Role selected")
    else:
        # Explicit outcome for the test contract
        assert target is not None
```

---

## Relationship to Element

`Elements` provides collection-level behavior (iteration, count-based waits, refresh).  
All interaction and validation is performed on the **individual `Element` items**.

```python
def test_first_row_text(results_page):
    results_page.rows.wait_until_found()

    first = results_page.rows[0]
    first.assert_visible()
    first.assert_text("First row")
```

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Element](/docs/reference/public-api/element.md)  
→ Next: [By](/docs/reference/public-api/by.md)
