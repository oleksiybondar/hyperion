← [Back to Documentation Index](/docs/index.md)  
← Previous: [By](/docs/reference/public-api/by.md)  
→ Next: [Expect](/docs/reference/public-api/expect.md)

---

# ActionBuilder

`ActionBuilder` composes and executes **low-level input interactions** (mouse, keyboard, touch).

It is conceptually similar to Selenium’s action chains, but follows Hyperion’s principles:

- actions are **composed explicitly** and executed at `perform()`
- **automatic structured logging** is built-in (action sequences are recorded and emitted)
- the builder is obtained from the **Page Object**, not created manually

Most tests should prefer `Element` helpers (`click()`, `fill()`, `drag_and_drop()`, etc.).  
Use `ActionBuilder` when you need an explicit multi-step gesture.

---

## Getting an ActionBuilder

`ActionBuilder` is accessed from the root Page Object:

```
builder = page.action_builder
```

You do not pass drivers or create adapters manually.

---

## Automatic logging (key Hyperion nuance)

When you build an action sequence, Hyperion records each action.  
When you call `perform()`, Hyperion emits a readable ordered sequence in logs.

This is intentionally automatic — action chains should be **debuggable by default**.

---

## Typed values

Some `ActionBuilder` methods accept values constrained by Hyperion typing.

### MouseButtonType

Mouse buttons are **lowercase strings** with the following allowed values:

- `"left"`
- `"middle"`
- `"right"`
- `"back"`
- `"forward"`

### TouchFingerType

Touch fingers are **lowercase strings** with the following allowed values:

- `"one"`
- `"two"`
- `"three"`
- `"four"`
- `"five"`

Passing unsupported values or incorrect casing (e.g. `"LEFT"`) is invalid.

---

## Method groups

`ActionBuilder` methods are designed for **chaining** and return the builder itself.

> Execution happens only when `perform()` is called.

---

## Mouse actions

### mouse_down(button: MouseButtonType) -> ActionBuilder

Press and hold a mouse button.

- `button`: one of `"left" | "middle" | "right" | "back" | "forward"`

### mouse_up(button: MouseButtonType) -> ActionBuilder

Release a mouse button.

- `button`: one of `"left" | "middle" | "right" | "back" | "forward"`

### mouse_move_to(x: float, y: float) -> ActionBuilder

Move the pointer to screen coordinates.

- `x`: x-coordinate
- `y`: y-coordinate

### click() -> ActionBuilder

Convenience left click (down + up).

### right_click() -> ActionBuilder

Convenience right click (down + up).

### click_by(x: float, y: float) -> ActionBuilder

Move to coordinates and left click.

### right_click_by(x: float, y: float) -> ActionBuilder

Move to coordinates and right click.

### click_on_element(element: Element) -> ActionBuilder

Click on the element center point.

### right_click_on_element(element: Element) -> ActionBuilder

Right click on the element center point.

Example:

```python
def test_context_menu(page, card):
    (
        page.action_builder
        .right_click_on_element(card)
        .perform()
    )

    page.context_menu.assert_visible()
```

---

## Keyboard actions

### key_down(key: str) -> ActionBuilder

Press and hold a key.

- `key`: backend key identifier (string)

### key_up(key: str) -> ActionBuilder

Release a key.

### key_press(key: str) -> ActionBuilder

Convenience key press (down + up).

### send_keys(keys: str) -> ActionBuilder

Send text input.

Example:

```python
def test_select_all_and_type(page):
    (
        page.action_builder
        .key_down("control")
        .key_press("a")
        .key_up("control")
        .send_keys("replacement text")
        .perform()
    )

    page.editor_value.assert_text("replacement text")
```

> Key identifiers are backend-dependent. Use values supported by your configured automation backend.

---

## Touch actions

### touch_down(finger: TouchFingerType) -> ActionBuilder

Simulate touch down.

- `finger`: one of `"one" | "two" | "three" | "four" | "five"`

### touch_up(finger: TouchFingerType) -> ActionBuilder

Simulate lifting a finger.

### touch_move_to(x: float, y: float, finger: TouchFingerType) -> ActionBuilder

Move a touch point.

- `x`: x-coordinate
- `y`: y-coordinate
- `finger`: one of `"one" | "two" | "three" | "four" | "five"`

### tap() -> ActionBuilder

Convenience tap using finger `"one"`.

### tap_by(x: float, y: float) -> ActionBuilder

Move finger `"one"` to coordinates and tap.

### tap_on_element(element: Element) -> ActionBuilder

Tap the element center point.

Example:

```python
def test_tap_primary_button(screen, primary_button):
    screen.action_builder.tap_on_element(primary_button).perform()
    screen.success_banner.assert_visible()
```

---

## Drag actions

### drag_and_drop_by(start_x: float, start_y: float, end_x: float, end_y: float) -> ActionBuilder

Drag from start coordinates to end coordinates.

### drag_element_by(element: Element, end_x: float, end_y: float) -> ActionBuilder

Drag an element from its center to end coordinates.

### drag_element_on_element(start_element: Element, end_element: Element) -> ActionBuilder

Drag one element and drop it onto another.

Example:

```python
def test_drag_card(board_page):
    (
        board_page.action_builder
        .drag_element_on_element(board_page.card, board_page.drop_zone)
        .perform()
    )

    board_page.drop_zone.assert_text("Card received")
```

---

## Timing inside a gesture

### wait(milliseconds: int) -> ActionBuilder

Insert a gesture-level delay into the action sequence.

- `milliseconds`: delay duration

This is intended for **gesture timing**, not UI synchronization.

For synchronization, use element waits / Wait API instead of action delays.

Example:

```python
page.action_builder.mouse_down("left").wait(250).mouse_up("left").perform()
```

---

## Executing actions

### perform(log: bool = True) -> ActionBuilder

Execute the composed sequence.

- `log`: when `True`, emits the recorded sequence into logs

Example:

```python
page.action_builder.click_by(10, 10).perform(log=False)
page.status_label.assert_visible()
```

---

## Summary

`ActionBuilder` is the low-level escape hatch for complex gestures:

- compose a chain of actions
- execute once via `perform()`
- rely on automatic structured logging for debuggability

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [By](/docs/reference/public-api/by.md)  
→ Next: [Expect](/docs/reference/public-api/expect.md)
