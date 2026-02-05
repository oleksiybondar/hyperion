← [Back to Documentation Index](/docs/index.md)  
← Previous: [Project Setup (pytest)](/docs/getting-started/project-setup-pytest.md)  
→ Next: [Quickstart: Web UI Testing](/docs/getting-started/quickstart-web.md)

---

# 1.3 Basic Configuration

This section explains the **basic configuration model** used by Hyperion.

Hyperion is designed so that:
- sensible defaults work out of the box
- configuration is **optional**
- you only override what you actually need

You can start writing tests without touching configuration at all.

---

## Where configuration lives

All configuration is exposed via the `hyperiontf.config` module.

Configuration is:
- global for the test run
- declarative
- usually set once (for example in `conftest.py`)

```python
from hyperiontf import config
```

You do not need to instantiate or initialize anything manually.

---

## Capabilities and automation backends

Capabilities define **how browsers or applications are started**.

In Hyperion, capabilities are:
- plain Python dictionaries
- backend-agnostic at the framework level
- passed through to the underlying automation engine

Hyperion consumes a small set of framework-level keys  
(e.g. `automation`, `browser`, `remote_url`) and forwards all other values as-is.

---

### Minimal web example (Selenium)

This is the smallest useful web configuration.

```python
from hyperiontf import config

config.web_capabilities = {
    "automation": "selenium",
    "browser": "chrome",
    "headless": True,
}
```

Notes:
- only keys you care about need to be defined
- everything else uses defaults
- browsers and drivers must exist on the system

---

### Playwright example (optional)

Playwright is supported but not required.

```python
from hyperiontf import config

config.web_capabilities = {
    "automation": "playwright",
    "browser": "webkit",
}
```

Important:
- Playwright browser binaries are **not** installed automatically
- see [1.1 Installation](/docs/getting-started/installation.md) for setup

---

### Mobile / desktop example (Appium)

Mobile and desktop automation is configured the same way:  
by providing an Appium-compatible capability dictionary.

The example below is **illustrative only**.

```python
from hyperiontf import config

config.mobile_capabilities = {
    "automation": "appium",
    "automationName": "XCUITest",
    "platformName": "iOS",
    "deviceName": "iPhone 14",
    "bundleId": "com.apple.mobilesafari",
}
```

All additional keys are passed directly to Appium.

---

## Logging configuration (optional)

Logging is enabled by default.

You may optionally change where logs are written:

```python
from hyperiontf import config

config.log.log_folder = "logs"
```

Most projects do not need additional logging configuration at the start.

---

## Timing, waits, and retries

Hyperion ships with **preconfigured timing defaults** for:
- element lookup
- waits
- retries
- stale recovery

You can override them if needed:

```python
from hyperiontf import config

config.element.wait_timeout = 30
config.element.search_attempts = 3
```

For early usage, it is recommended to **keep the defaults**.

---

## What you can safely ignore for now

When getting started, you do **not** need to configure:

- locator resolution rules
- retry semantics
- context switching behavior
- logging formatters
- advanced backend options

These topics are covered later in the documentation.

---

## Summary

For basic usage:

- configuration is optional
- capabilities are simple dictionaries
- defaults are safe and intentional
- only override what you understand and need

Once configuration is in place, you are ready to run end-to-end tests.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Project Setup (pytest)](/docs/getting-started/project-setup-pytest.md)  
→ Next: [Quickstart: Web UI Testing](/docs/getting-started/quickstart-web.md)
