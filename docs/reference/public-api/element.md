[← Widget](/docs/reference/public-api/widget.md) | [Elements →](/docs/reference/public-api/elements.md)

# Element

`Element` is Hyperion’s **leaf-level interaction unit**.

It represents a single UI node (button, input, label, etc.) and provides the **core interaction API** reused by `Widget`, `IFrame`, `WebView`, and page-like containers.

You typically **do not instantiate `Element` directly**.  
Elements are declared on Page Objects via `@element` and resolved by Hyperion at interaction time.

---

## Conceptual role

| Aspect | Meaning |
|---|---|
| Structural container | No (leaf node) |
| Hierarchical | Yes (belongs to a parent container) |
| Interaction API | Yes (primary user interaction surface) |
| Context boundary | No (inherits context from parent container) |
| Stability model | Retries + recovery are applied automatically |

---

## Public properties

### location: rect-like

Alias for `get_location()`.

### size: rect-like

Alias for `get_size()`.

### rect: rect-like

Alias for `get_rect()`.

### is_present: bool

Whether the element is currently present in the UI tree.

> “rect-like” means an object/mapping with coordinates and dimensions (commonly: `x`, `y`, `width`, `height`).

---

## Interactions

Element interactions are designed for **stable automation**:
- resilience against transient UI issues (stale references, brief DOM mutations)
- intended to be used together with **interactive waits**, not passive sleeping

### click() -> None

Clicks the element.

### right_click() -> None

Right-clicks the element.

### send_keys(data: str | list[str]) -> None

Types into the element.

- `data`: either a single string or a list of strings/keys supported by the backend.

### fill(data: str | list[str]) -> None

Alias for `send_keys()`.

### clear() -> None

Clears an input field.

### clear_and_fill(data: str | list[str]) -> None

Clears the input, then types the provided value.

### submit() -> None

Submits a form element (when applicable).

### scroll_into_view(force: bool = False) -> None

Scrolls the element into view.

- `force`: when `True`, forces scroll behavior even if the element is considered in view.

### drag_and_drop_by(x: int, y: int) -> None

Drags the element by an offset.

- `x`: horizontal offset
- `y`: vertical offset

### drag_and_drop(other: Element) -> None

Drags this element onto another element.

- `other`: target element

---

## Minimal interaction example

```python
from hyperiontf import WebPage, element, By


class LoginPage(WebPage):

    @element
    def username(self):
        return By.id("username")

    @element
    def password(self):
        return By.id("password")

    @element
    def submit_btn(self):
        return By.css("button[type='submit']")


page = LoginPage.start_browser()
page.open(my_url)

page.username.wait_until_visible()
page.username.clear_and_fill("alice")

page.password.clear_and_fill("correct-horse-battery-staple")
page.submit_btn.click()
```

---

## Content and attribute accessors

### get_text() -> str

Returns element text.

### get_attribute(name: str) -> str | None

Returns the attribute value.

- `name`: attribute name

### get_style(name: str) -> str | None

Returns the computed style value for a style property.

- `name`: style property name

### get_location() -> dict

Returns element location info.

### get_size() -> dict

Returns element size info.

### get_rect() -> dict

Returns element rect info with keys such as `x`, `y`, `width`, `height`.

---

## State checks

State checks return `bool`. They do not wait; use waits when synchronization is required.

### is_visible() -> bool

True if element is visible.

### is_hidden() -> bool

True if element is hidden.

### is_enabled() -> bool

True if element is enabled.

### is_disabled() -> bool

True if element is disabled.

### is_selected() -> bool

True if element is selected (checkbox/radio/etc.).

---

## Waits

Element waits are **interactive**:
- actively re-check the condition until satisfied or timeout occurs
- integrate with Hyperion retries and recovery
- replace passive sleeping in stable test design

### wait_until_found() -> None

Waits until the element becomes present.

### wait_until_missing() -> None

Waits until the element becomes not present.

### wait_until_visible() -> None

Waits until the element becomes visible.

### wait_until_hidden() -> None

Waits until the element becomes hidden.

### wait_until_enabled() -> None

Waits until the element becomes enabled.

### wait_until_interactable() -> None

Waits until the element is visible and enabled (ready for user interaction).

### wait_until_animation_completed() -> None

Waits until the element’s geometry stabilizes (no ongoing animation).

### wait_until_fully_interactable() -> None

Waits until the element is visible + enabled + animation completed.

---

## Default timing behavior

Element operations rely on framework configuration defaults for baseline stability.

| Setting | Default |
|---|---:|
| `search_attempts` | `3` |
| `search_retry_timeout` | `0.5` |
| `stale_recovery_timeout` | `0.5` |
| `wait_timeout` | `30` |
| `missing_timeout` | `5` |

> Configuration is centralized in Hyperion configuration. Element methods use these values as default behavior.

---

## Assertions

Assertion methods are **blocking**:
- on failure they raise immediately
- intended for test-defining outcomes
- tests should always end with explicit `assert_*` calls

### assert_text(expected_text) -> None

Asserts element text equals expected.

### assert_attribute(name, expected_value) -> None

Asserts attribute equals expected.

### assert_style(name, expected_value) -> None

Asserts computed style property equals expected.

### assert_visible() -> None

Asserts element is visible.

### assert_hidden() -> None

Asserts element is hidden.

### assert_enabled() -> None

Asserts element is enabled.

### assert_disabled() -> None

Asserts element is disabled.

### assert_selected() -> None

Asserts element is selected.

#### Minimal assertion example

```python
# ... after submitting a form
page.error_banner.assert_hidden()
page.welcome_text.assert_text("Welcome, Alice")
```

---

## Verifications

Verification methods return an **`ExpectationResult`**:

- structured result used for **decision logging**
- casts to `bool` for use in branching logic
- does **not** replace assertions (tests must still end with `assert_*`)

### verify_text(expected_text) -> ExpectationResult

### verify_attribute(name, expected_value) -> ExpectationResult

### verify_style(name, expected_value) -> ExpectationResult

### verify_visible() -> ExpectationResult

### verify_hidden() -> ExpectationResult

### verify_enabled() -> ExpectationResult

### verify_disabled() -> ExpectationResult

### verify_selected() -> ExpectationResult

#### Typical verify usage (branching + explicit end assertion)

```python
result = page.error_banner.verify_visible()

if result:
    # Decision is logged and traceable
    page.error_banner.screenshot("Validation error displayed")
else:
    # Still end with an explicit assertion for the test contract
    page.welcome_text.assert_text("Welcome, Alice")
```

---

## Screenshots

### make_screenshot(filepath: str | None = None) -> Image

Captures an element screenshot and returns an `Image` object.

- `filepath`: optional destination path used when creating the returned `Image`

### screenshot(message: str = "...", title: str = "...") -> None

Logs an element screenshot as an attachment, with optional message/title.

---

## Visual checks (element level)

Element visual checks compare current rendering against an expected image (or collect a baseline, depending on visual mode).

### Visual defaults

| Setting | Default |
|---|---:|
| `mode` | `VisualMode.COMPARE` |
| `default_mismatch_threshold` | `5.0` |
| `default_partial_mismatch_threshold` | `0.5` |

### Region format

Regions are rectangles with keys:

- `x`, `y`, `width`, `height`

### verify_visual_match(...) -> ImageExpectationResult

Full visual comparison (optionally with include/exclude regions).

### assert_visual_match(...) -> ImageExpectationResult

Blocking version of `verify_visual_match(...)`.

### verify_visual_match_in_regions(...) -> ImageExpectationResult

Focused comparison in specific regions.

### assert_visual_match_in_regions(...) -> ImageExpectationResult

Blocking version of `verify_visual_match_in_regions(...)`.

### verify_visual_exclusion_match(...) -> ImageExpectationResult

Comparison excluding regions.

### assert_visual_exclusion_match(...) -> ImageExpectationResult

Blocking version of `verify_visual_exclusion_match(...)`.

#### Minimal visual assertion example

```python
# Compare the whole element against a stored reference image
page.header_logo.assert_visual_match("/tmp/baselines/logo.png")
```

#### Minimal visual verification example (exclude a dynamic region)

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

## EQL integration (leaf behavior)

`Element` is a **leaf** in the hierarchy, so EQL selection does not traverse beneath an element.

Within EQL attribute resolution, `Element` supports:
- `text` → `get_text()`
- `style.<name>` → `get_style(<name>)`
- `<attribute>` → `get_attribute(<attribute>)`

---

## Practical guidance

- Prefer **wait + interact** over passive delays.
- Prefer **`assert_*`** for outcomes and test contracts.
- Use **`verify_*`** for branching and decision traceability, then end with assertions.
- Use element-level visual checks when you need pixel-level confidence for a specific component.

---

[← Widget](/docs/reference/public-api/widget.md) | [Elements →](/docs/reference/public-api/elements.md)