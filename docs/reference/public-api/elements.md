[← Element](/docs/reference/public-api/element.md) [IFrame →](/docs/reference/public-api/iframe.md)

# Elements

`Elements` represents a **collection of `Element` objects** resolved from a single locator.

- Use it when a locator matches **multiple nodes** (rows, items, cards, chips, etc.).
- Iterating or indexing yields regular `Element` instances (with the full `Element` interaction/wait/assert/verify API).
- `Elements` also supports **EQL-powered selection** via string indexing.

> `Elements` is a collection of leaves — it is not a structural container like `Widget`.

---

## Creating `Elements`

You typically define an `Elements` field on a `WebPage`/`Widget`/`IFrame`/`WebView` using a locator that matches multiple items.

{codeblock}
from hyperiontf import WebPage
from hyperiontf.ui import By

class ResultsPage(WebPage):
    rows = By.css(".result-row").elements("Result rows")
{codeblock}

---

## Collection behavior

### Length

| Operation | Result |
|---|---|
| `len(elements)` | number of currently resolved items |

{codeblock}
assert len(page.rows) >= 1
{codeblock}

### Iteration

`Elements` is iterable and yields `Element` items.

{codeblock}
for row in page.rows:
    row.assert_visible()
{codeblock}

### Indexing

| Operation | Result |
|---|---|
| `elements[0]` | first `Element` |
| `elements[-1]` | last `Element` |
| `elements[i]` | `Element` at index `i` |

{codeblock}
page.rows[0].click()
page.rows[-1].scroll_into_view()
{codeblock}

### Membership and list-like helpers

`Elements` exposes list-like helpers over the cached item list.

| Method | Meaning |
|---|---|
| `item in elements` | membership test |
| `elements.index(item)` | index of a specific `Element` instance |
| `elements.count(item)` | count of a specific `Element` instance |
| `elements.sort(key=..., reverse=...)` | sort cached items (does not change DOM order) |

---

## Presence

| Property | Type | Meaning |
|---|---:|---|
| `is_present` | `bool` | `True` if at least one item is present, otherwise `False` |

**Notes**
- `is_present` answers “is there at least one match right now?”
- For “wait until at least one exists”, use `wait_until_found()`.

---

## Cache and refresh behavior

`Elements` caches resolved items and refreshes the cache when the underlying result count changes.

| Method | Behavior |
|---|---|
| `force_refresh()` | clears internal cache and re-finds the collection |

Use `force_refresh()` when the UI updates and you want to re-evaluate matches immediately (for example, after applying filters).

---

## Waits on collections

All waits are **interactive** (polling + retries), not passive sleeping.

| Method | Waits for |
|---|---|
| `wait_until_found()` | at least one item exists |
| `wait_until_missing()` | no items exist |
| `wait_until_items_count(expected_count)` | item count equals `expected_count` |
| `wait_until_items_decrease()` | item count decreases compared to the previous observation |
| `wait_until_items_increase()` | item count increases compared to the previous observation |
| `wait_until_items_change()` | item count changes (increase or decrease) compared to the previous observation |

### Example: wait for results to load

{codeblock}
page.rows.wait_until_found()
assert len(page.rows) > 0
{codeblock}

### Example: wait for list to refresh after filtering

{codeblock}
page.filter_button.click()

# wait until the result count changes (either up or down)
page.rows.wait_until_items_change()

# end with explicit assertions
assert len(page.rows) >= 1
page.rows[0].assert_visible()
{codeblock}

---

## EQL selection on collections

`Elements` supports **EQL-powered lookup** via string indexing:

- `elements["<EQL query>"] -> Element | None`
- The query is evaluated against each item.
- The first match is returned.
- If nothing matches, `None` is returned.

This enables **semantic selection** within a collection, avoiding brittle index-based tests.

### Supported element attributes in EQL

When evaluating an EQL expression against an `Element`, Hyperion resolves:

| EQL attribute | Maps to |
|---|---|
| `text` | `Element.get_text()` |
| `style.<name>` | `Element.get_style(<name>)` |
| `<attribute_name>` | `Element.get_attribute(<attribute_name>)` |

> EQL syntax itself (operators, grouping, etc.) is defined by the EQL language. In API reference pages we document the integration points and supported attributes.

### Example: select a row by visible text

{codeblock}
row = page.rows['text == "Coffee Mug"']
assert row is not None

row.click()
{codeblock}

### Example: select by attribute (stable test id)

{codeblock}
item = page.rows['data_test_id == "result-42"']
assert item is not None

item.assert_visible()
{codeblock}

### Example: select by computed style

{codeblock}
# Example: select an item that is visually marked as "active"
active = page.rows['style.color == "rgba(0, 0, 0, 1)"']
assert active is not None

active.click()
{codeblock}

### Guidance for EQL in tests

- Prefer EQL for **meaningful selection** (“the row with title X”), especially when list order is unstable.
- Handle the “not found” case explicitly:
  - assert that a match was found (`assert match is not None`)
  - or branch intentionally using `if match: ...` (then still end with explicit assertions)

{codeblock}
target = page.rows['text == "Admin"']

if target:
    target.click()
    page.toast.assert_text("Role selected")
else:
    page.rows.wait_until_found()
    assert target is not None  # explicit test outcome
{codeblock}

---

## Relationship to `Element`

- `Elements` provides collection-level operations and waits.
- **All interactions, assertions, verifications, and visual checks** are performed on individual items (`Element`) obtained from the collection.

{codeblock}
page.rows.wait_until_found()

page.rows[0].assert_visible()
page.rows[0].assert_text("First row")
{codeblock}

---

[← Element](/docs/reference/public-api/element.md) | [IFrame →](/docs/reference/public-api/iframe.md)