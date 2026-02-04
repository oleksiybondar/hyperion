[← Widget](/docs/reference/public-api/widget.md) | [Elements →](/docs/reference/public-api/elements.md)

# Element

`Element` is Hyperion’s **leaf-level interaction unit**.

- It represents a single UI node (for example: button, input, label).
- It is the **core interaction API** reused by higher-level objects (such as `Widget`, `IFrame`, `WebView`, and `Page`-like containers).
- It provides:
  - user-like interactions (click, type, drag-and-drop, scrolling)
  - interactive waits (found/visible/enabled/interactable/hidden, animation completion)
  - explicit assertions (`assert_*`)
  - traceable decision logging (`verify_*`)
  - element-level visual checks

> Elements are usually defined as attributes on `Widget`/`Page`/`IFrame`/`WebView` objects. You typically do **not** instantiate `Element` directly.

---

## Public properties

| Property | Type | Meaning |
|---|---:|---|
| `location` | rect-like | Alias for `get_location()` |
| `size` | rect-like | Alias for `get_size()` |
| `rect` | rect-like | Alias for `get_rect()` |
| `is_present` | `bool` | Whether the element is currently present in the UI tree |

**Notes**
- “rect-like” means a mapping/object with coordinates and dimensions (commonly: `x`, `y`, `width`, `height`).

---

## Interaction methods

All interaction methods are designed for **stable automation**:
- They execute with built-in resilience against transient UI issues (for example: stale references or short-lived DOM mutations).
- They are meant to be used together with Hyperion waits (instead of passive sleeping).

| Method | Signature | What it does |
|---|---|---|
| `click()` | `click() -> None` | Clicks the element |
| `right_click()` | `right_click() -> None` | Right-clicks the element |
| `send_keys()` | `send_keys(data: str | list[str]) -> None` | Types input into the element |
| `fill` | alias | Alias for `send_keys()` |
| `clear()` | `clear() -> None` | Clears an input field |
| `clear_and_fill()` | `clear_and_fill(data: str | list[str]) -> None` | Clears then types input |
| `submit()` | `submit() -> None` | Submits a form element (if applicable) |
| `scroll_into_view()` | `scroll_into_view(force: bool = False) -> None` | Scrolls element into view |
| `drag_and_drop_by()` | `drag_and_drop_by(x: int, y: int) -> None` | Drags the element by an offset |
| `drag_and_drop()` | `drag_and_drop(other: Element) -> None` | Drags onto another element |

### Minimal interaction example

```python
from hyperiontf import WebPage
from hyperiontf.ui import By

class LoginPage(WebPage):
    username = By.id("username").element("Username")
    password = By.id("password").element("Password")
    submit_btn = By.css("button[type='submit']").element("Submit")

page = LoginPage(driver)

page.username.wait_until_visible()
page.username.clear_and_fill("alice")

page.password.clear_and_fill("correct-horse-battery-staple")
page.submit_btn.click()
```

---

## Content and attribute access

| Method | Signature | Returns |
|---|---|---|
| `get_text()` | `get_text() -> str` | Element text |
| `get_attribute()` | `get_attribute(name: str) -> str | None` | Attribute value |
| `get_style()` | `get_style(name: str) -> str | None` | Computed style value (style property by name) |
| `get_location()` | `get_location() -> dict` | Location info |
| `get_size()` | `get_size() -> dict` | Size info |
| `get_rect()` | `get_rect() -> dict` | Rect info (`x`,`y`,`width`,`height`) |

---

## State checks

| Method | Signature | Meaning |
|---|---|---|
| `is_visible()` | `is_visible() -> bool` | Element is visible |
| `is_hidden()` | `is_hidden() -> bool` | Element is hidden |
| `is_enabled()` | `is_enabled() -> bool` | Element is enabled |
| `is_disabled()` | `is_disabled() -> bool` | Element is disabled |
| `is_selected()` | `is_selected() -> bool` | Element is selected (checkbox/radio/etc.) |

---

## Waits

Element waits are **interactive**:
- they actively re-check the condition until it is satisfied or a timeout is reached
- they are intended to replace passive sleeping
- they integrate with Hyperion’s stability model (retries and recovery)

| Method | Waits for |
|---|---|
| `wait_until_found()` | element becomes present |
| `wait_until_missing()` | element becomes not present |
| `wait_until_visible()` | element becomes visible |
| `wait_until_hidden()` | element becomes hidden |
| `wait_until_enabled()` | element becomes enabled |
| `wait_until_interactable()` | element becomes visible and enabled (ready for user interaction) |
| `wait_until_animation_completed()` | element’s geometry stabilizes (no ongoing animation) |
| `wait_until_fully_interactable()` | visible + enabled + animation completed |

### Defaults used by Element (framework configuration)

These defaults define baseline stability behavior (search retries, recovery timeouts, and wait timeouts):

| Setting | Default |
|---|---:|
| `search_attempts` | `3` |
| `search_retry_timeout` | `0.5` |
| `stale_recovery_timeout` | `0.5` |
| `wait_timeout` | `30` |
| `missing_timeout` | `5` |

> Exact configuration is centralized in Hyperion configuration. Element methods rely on these values as their default behavior.

---

## Assertions: `assert_*`

Assertion methods are **blocking**:
- they are meant to be used as **test-ending or test-defining checks**
- on failure, they stop the test flow (by raising)

| Method | Purpose |
|---|---|
| `assert_text(expected_text)` | Assert element text equals expected |
| `assert_attribute(name, expected_value)` | Assert attribute equals expected |
| `assert_style(name, expected_value)` | Assert style property equals expected |
| `assert_visible()` | Assert element is visible |
| `assert_hidden()` | Assert element is hidden |
| `assert_enabled()` | Assert element is enabled |
| `assert_disabled()` | Assert element is disabled |
| `assert_selected()` | Assert element is selected |

### Minimal assertion example

```python
# ... after submitting a form
page.error_banner.assert_hidden()
page.welcome_text.assert_text("Welcome, Alice")
```

---

## Verifications: `verify_*`

Verification methods return an **`ExpectationResult`** object:

- It is a structured result for **decision logging and traceability**
- It **casts to `bool`**, so it can be used in conditionals and comparisons
- It does **not** replace test assertions: tests should still end with explicit `assert_*` checks

| Method | Returns |
|---|---|
| `verify_text(expected_text)` | `ExpectationResult` |
| `verify_attribute(name, expected_value)` | `ExpectationResult` |
| `verify_style(name, expected_value)` | `ExpectationResult` |
| `verify_visible()` | `ExpectationResult` |
| `verify_hidden()` | `ExpectationResult` |
| `verify_enabled()` | `ExpectationResult` |
| `verify_disabled()` | `ExpectationResult` |
| `verify_selected()` | `ExpectationResult` |

### Typical verify usage (branching + explicit end assertion)

```python
result = page.error_banner.verify_visible()

if result:
    # branch logic (decision is logged)
    page.error_banner.screenshot("Validation error displayed")
else:
    # still end with an explicit assertion for the test contract
    page.welcome_text.assert_text("Welcome, Alice")
```

---

## Screenshots

### Element image object

| Method | Signature | Behavior |
|---|---|---|
| `make_screenshot()` | `make_screenshot(filepath: str | None = None) -> Image` | Captures an element screenshot and returns it as an `Image` object |

- If `filepath` is provided, the returned `Image` is created with that path and the captured image data.

### Log an element screenshot

| Method | Signature | Behavior |
|---|---|---|
| `screenshot()` | `screenshot(message: str = "...", title: str = "...") -> None` | Logs an element screenshot as an attachment with message/title |

---

## Visual assertions (element level)

Element visual checks compare the element’s current rendering against an expected image (or collect a baseline, depending on visual mode).

### Defaults (visual configuration)

| Setting | Default |
|---|---:|
| `mode` | `VisualMode.COMPARE` |
| `default_mismatch_threshold` | `5.0` |
| `default_partial_mismatch_threshold` | `0.5` |

### Regions format

Visual region lists use rectangle objects with the following keys:

- `x`, `y`, `width`, `height`

### Visual methods

| Method | Signature | Notes |
|---|---|---|
| `verify_visual_match(...)` | `verify_visual_match(expected_value, mismatch_threshold=..., compare_regions=None, exclude_regions=None, mode=...) -> ImageExpectationResult` | Full visual comparison (with optional include/exclude regions) |
| `assert_visual_match(...)` | same args/return | Blocking version |
| `verify_visual_match_in_regions(...)` | `verify_visual_match_in_regions(expected_value, compare_regions=None, mismatch_threshold=..., mode=...) -> ImageExpectationResult` | Focused comparison in specific regions |
| `assert_visual_match_in_regions(...)` | same args/return | Blocking version |
| `verify_visual_exclusion_match(...)` | `verify_visual_exclusion_match(expected_value, exclude_regions=None, mismatch_threshold=..., mode=...) -> ImageExpectationResult` | Comparison excluding regions |
| `assert_visual_exclusion_match(...)` | same args/return | Blocking version |

### Minimal visual assertion example

```python
# Compare the whole element against a stored reference image
page.header_logo.assert_visual_match("/tmp/baselines/logo.png")
```

### Minimal visual verification example (exclude a dynamic region)

```python
exclude = [{"x": 120, "y": 10, "width": 80, "height": 20}]  # e.g. dynamic timestamp area
result = page.summary_card.verify_visual_exclusion_match(
    "/tmp/baselines/summary.png",
    exclude_regions=exclude,
)

if result:
    page.summary_card.assert_visible()
else:
    page.summary_card.screenshot("Visual mismatch detected")
    page.summary_card.assert_visual_exclusion_match(
        "/tmp/baselines/summary.png",
        exclude_regions=exclude,
    )
```

---

## EQL integration (element leaf behavior)

`Element` is a **leaf** in the hierarchy, so EQL resolution does not allow child selection beneath an element.

Within EQL attribute resolution, `Element` supports:
- `text` (mapped to `get_text()`)
- `style.<name>` (mapped to `get_style(<name>)`)
- `<attribute>` (mapped to `get_attribute(<attribute>)`)

> For the full EQL syntax and selection model, see the EQL documentation section (outside this API reference page).

---

## Practical guidance (API usage)

- Prefer **wait + interact** over passive delays.
- Prefer **`assert_*`** for test outcomes.
- Use **`verify_*`** for branching decisions and traceability, then end with explicit assertions.
- Use element-level visual checks when you need pixel-level confidence for a specific UI component.

---

[← Widget](/docs/reference/public-api/widget.md) | [Elements →](/docs/reference/public-api/elements.md)