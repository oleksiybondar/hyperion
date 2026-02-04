# 5.3 DesktopWindow

← [/docs/reference/public-api/mobilescreen.md](/docs/reference/public-api/mobilescreen.md)  
→ [/docs/reference/public-api/widget.md](/docs/reference/public-api/widget.md)

---

`DesktopWindow` is the root Page Object for **desktop application automation** in Hyperion.

Use it to:
- launch and control native desktop applications
- model windows as a hierarchy of widgets and elements
- interact with desktop UI through Hyperion’s stable, logged APIs

Desktop automation in Hyperion follows the **same mental model** as web and mobile:
hierarchy-first Page Objects, automatic context handling, and explicit assertions.

---

## Import

```python
from hyperiontf import DesktopWindow
```

---

## Launching a desktop session

### `DesktopWindow.launch_app(caps: dict | None = None, attempts: int = ...) -> DesktopWindow`

Launches a desktop automation session and returns an instance of your window class.

#### `caps`
`caps` can be:
- `None` (or omitted): use the default desktop configuration
- `dict`: explicitly define capabilities for this session

#### Important note about capabilities
Hyperion does **not** define its own desktop capability schema.

- Hyperion uses a small set of **routing keys** (such as `automation`) to select an automation backend.
- All other capability keys are passed through to the underlying desktop automation tool.
- For authoritative and complete capability definitions, refer to:
  - Appium Desktop / Mac2 / Windows capabilities
  - WinAppDriver capabilities
  - AutoIt / xdotool / pyautogui documentation (when applicable)

Hyperion documentation provides **patterns and examples**, not a replacement for official capability references.

---

## Capabilities keys (desktop)

### `automation`
Selects the automation backend for desktop sessions.

Common values include:
- `appium`
- `windows application driver`
- `autoit`
- `xdotool`
- `pyautogui`

### `automationName`
Used with Appium-based desktop automation.

Common values include:
- `Mac`
- `Windows`

### Other common desktop capability keys
Shown here only as illustrative examples:

- `platformName` (e.g. `Mac`, `Windows`)
- `deviceName`
- application identity keys (e.g. `app`, `bundleId`)
- environment/server keys (for example `remote_url`)

---

## Examples

### macOS application (Appium / Mac2)

```python
from hyperiontf import DesktopWindow


class DesktopCalculator(DesktopWindow):
    pass


caps = {
    "automation": "appium",
    "automationName": "Mac",
    "platformName": "Mac",
    "deviceName": "Mac",
    "bundleId": "com.apple.calculator",
    "remote_url": "http://127.0.0.1:4723",
}

page = DesktopCalculator.launch_app(caps)
```

### Windows application (WinAppDriver-style)

```python
from hyperiontf import DesktopWindow


class WindowsCalculator(DesktopWindow):
    pass


caps = {
    "automation": "windows application driver",
    "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
}

page = WindowsCalculator.launch_app(caps)
```

---

## Window model and hierarchy

A `DesktopWindow` represents the **root window** of an application.

Inside it, you model:
- widgets (panels, toolbars, dialogs)
- elements (buttons, inputs, labels)

The same rules apply as everywhere else in Hyperion:
- parent containers resolve themselves automatically
- manual window switching is usually a design smell
- structure belongs in Page Objects, not tests

---

## Inherited API

`DesktopWindow` inherits common Page Object capabilities.

### `action_builder`
Fluent API for advanced interactions (mouse/keyboard/touch) with full logging.

See: → [/docs/reference/public-api/action-builder.md](/docs/reference/public-api/action-builder.md)

### `quit() -> None`
Closes the desktop automation session.

### `make_screenshot(filepath: str | None = None)`
Captures a screenshot and returns it as an image object.

### `screenshot(message: str = ..., title: str = ...) -> None`
Captures and attaches a screenshot to the test log.

### Visual helpers
Page objects also provide visual verification helpers such as
`verify_visual_match(...)` and `assert_visual_match(...)`.

See: → [/docs/reference/public-api/visual.md](/docs/reference/public-api/visual.md)

---

## Recommended usage pattern

Model window structure declaratively and expose behavior through methods.

```python
from hyperiontf import DesktopWindow, element, By, expect


class CalculatorWindow(DesktopWindow):

    @element
    def display(self):
        return By.accessibility_id("CalculatorResults")

    @element
    def add_button(self):
        return By.accessibility_id("plusButton")

    def add(self, a: int, b: int) -> None:
        self.display.clear()
        self.display.fill(str(a))
        self.add_button.click()
        self.display.fill(str(b))


def test_desktop_calculation():
    page = CalculatorWindow.launch_app()
    page.add(2, 3)

    expect(page.display.get_text()).to_contain("5")

    page.quit()
```

---

← [/docs/reference/public-api/mobilescreen.md](/docs/reference/public-api/mobilescreen.md)  
→ [/docs/reference/public-api/widget.md](/docs/reference/public-api/widget.md)