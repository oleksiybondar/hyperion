# 5.2 MobileScreen

← [/docs/reference/public-api/webpage.md](/docs/reference/public-api/webpage.md)  
→ [/docs/reference/public-api/desktopwindow.md](/docs/reference/public-api/desktopwindow.md)

---

`MobileScreen` is the root Page Object for **mobile UI automation** in Hyperion.

Use it to:
- launch a mobile app session (typically via Appium)
- model screens as a hierarchy of elements/widgets/webviews
- interact through Hyperion’s stable, logged APIs (with automatic context/content handling)

---

## Import

```
from hyperiontf import MobileScreen
```

---

## Launching a mobile session

### `MobileScreen.launch_app(caps: dict | None = None, attempts: int = ...) -> MobileScreen`

Launches a mobile automation session and returns an instance of your screen class.

#### `caps`
`caps` can be:
- `None` (or omitted): use the default configuration (the framework’s “standard settings”)
- `dict`: explicitly define capabilities for this session

#### Important note about capabilities
Hyperion does **not** define its own “official capabilities schema”.

- Hyperion uses a few **routing-friendly keys** (like `automation`) to pick an automation backend.
- Everything else should be treated as **tool/vendor capabilities**.
- For authoritative capability keys and values, refer to the documentation of the underlying tool/provider you use:
  - Appium capabilities (including iOS/Android specifics)
  - WinAppDriver capabilities (desktop; see `/docs/reference/public-api/desktopwindow.md`)

Hyperion’s documentation will show **examples** and **common patterns**, but the source of truth for capability options is the tool itself.

---

## Capabilities keys (mobile)

### `automation`
Selects the automation backend for mobile sessions.

Supported value (mobile):
- `appium`

### `automationName`
Selects the Appium automation driver.

Common values include (not exhaustive):
- `UiAutomator2` (Android)
- `XCUITest` (iOS)
- `Mac` / `Windows` / `Espresso` (environment-dependent)

### Other common Appium capability keys
These are standard Appium concepts, shown here only to make examples readable:

- `platformName` (e.g., `Android`, `iOS`)
- `platformVersion`
- `deviceName`
- app identity keys (vary by platform), for example:
  - Android: `appPackage`, `appActivity`
  - iOS: `bundleId`
- environment/server keys (when applicable), for example:
  - `remote_url`

---

## Examples

### Android app session

```python
from hyperiontf import MobileScreen


class MobileCalculator(MobileScreen):
    pass


caps = {
    "automation": "appium",
    "automationName": "UiAutomator2",
    "platformName": "Android",
    "platformVersion": "12.0",
    "appPackage": "com.google.android.calculator",
    "appActivity": "com.android.calculator2.Calculator",
    "uiautomator2ServerInstallTimeout": 60000,
}

page = MobileCalculator.launch_app(caps)
```

### iOS hybrid session (native + Safari WebView)

A common “hybrid” pattern is using a native session and then interacting with web content (Safari/webviews).
Hyperion’s model stays the same: keep a hierarchy-first Page Object and let Hyperion handle context/content transitions.

```python
from hyperiontf import MobileScreen


class HybridCalculator(MobileScreen):
    pass


caps = {
    "automation": "appium",
    "automationName": "XCUITest",
    "platformName": "iOS",
    "deviceName": "iPhone 14",
    "bundleId": "com.apple.mobilesafari",
    "includeSafariInWebviews": True,
    "wdaLaunchTimeout": 3000,
    "usePrebuiltWDA": True,
}

page = HybridCalculator.launch_app(caps)
```

---

## WebViews and content on mobile

On mobile, your app may expose web content (WebViews) alongside native UI.
In Hyperion, WebViews are modeled as **nested page objects** inside the screen hierarchy.

Key ideas:
- keep your Page Object structure stable (screen → widget → webview → elements)
- avoid manual context switching in tests; if you feel you need it, treat it as a design smell and move the concern into the Page Object layer

See:
- → [/docs/how-to/work-with-webviews.md](/docs/how-to/work-with-webviews.md)
- → [/docs/how-to/work-with-iframes.md](/docs/how-to/work-with-iframes.md)

---

## Inherited API

`MobileScreen` inherits common Page Object capabilities.

### `action_builder`
Fluent API for advanced interactions (mouse/keyboard/touch) with full logging.

See: → [/docs/reference/public-api/action-builder.md](/docs/reference/public-api/action-builder.md)

### `quit() -> None`
Closes the session.

### `make_screenshot(filepath: str | None = None)`
Captures a screenshot and returns it as an image object.

### `screenshot(message: str = ..., title: str = ...) -> None`
Captures and attaches a screenshot to the test log.

### Visual helpers
Page objects also provide visual verification helpers such as `verify_visual_match(...)` and `assert_visual_match(...)`.

See: → [/docs/reference/public-api/visual.md](/docs/reference/public-api/visual.md)

---

## Recommended usage pattern

Model UI structure with `@element` / `@widget(s)` / `@webview` and model screen behavior with methods.
Keep tests focused on intent and assertions.

```python
from hyperiontf import MobileScreen, element, By, expect


class LoginScreen(MobileScreen):

    @element
    def email_input(self):
        return By.id("email")

    @element
    def password_input(self):
        return By.id("password")

    @element
    def sign_in_button(self):
        return By.id("sign-in")

    def sign_in(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.sign_in_button.click()


def test_login():
    page = LoginScreen.launch_app()
    page.sign_in("user@example.com", "secret")

    # End with an explicit assertion
    expect(page.sign_in_button.is_visible()).to_be(False)

    page.quit()
```

---

← [/docs/reference/public-api/webpage.md](/docs/reference/public-api/webpage.md)  
→ [/docs/reference/public-api/desktopwindow.md](/docs/reference/public-api/desktopwindow.md)