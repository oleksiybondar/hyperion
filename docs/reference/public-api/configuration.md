← [Back to Documentation Index](/docs/index.md)  
← Previous: [Visual Testing API](/docs/reference/public-api/visual.md)  
→ Next: [Exceptions](/docs/reference/public-api/exceptions.md)

---

# 5.18 Configuration

Hyperion provides a **global, singleton configuration object** that controls framework behavior across all subsystems:
execution, logging, stability, capabilities, REST, visual testing, and CLI integration.

Configuration is **not constructed by users**.  
It is initialized once and accessed everywhere via a shared singleton.

---

## Accessing configuration

The configuration object is available as `config`:

```python
from hyperiontf import config
```

All configuration is applied by mutating attributes on this object **before test execution begins**.

---

## Configuration lifecycle and guarantees

Hyperion configuration follows these rules:

- configuration is a **singleton**
- loaded once per process
- shared across tests, Page Objects, widgets, and framework internals
- may be updated programmatically or from a file
- values are read dynamically by the framework at runtime

There is no need to pass configuration values through APIs.

---

## Loading configuration from files

Hyperion supports loading configuration from:

- `.cfg`
- `.json`
- `.yml` / `.yaml`

To load configuration from a file:

```python
from hyperiontf import config

config.update_from_cfg_file("hyperion_config.yaml")
```

### Section name mapping

- Top-level keys in JSON/YAML or section names in `.cfg` files
  are mapped to config attributes using **snake_case**.
- CamelCase section names are also supported and normalized internally.

Example (YAML):

```python
pageObject:
  startRetries: 5
  viewportLg: 1024
```

---

## Configuration sections overview

The configuration object exposes the following public sections:

- `config.logger`
- `config.page_object`
- `config.element`
- `config.web_capabilities`
- `config.mobile_capabilities`
- `config.desktop_capabilities`
- `config.rest`
- `config.visual`
- `config.cli`

Each section is a structured object with documented attributes.

---

## Logger configuration (`config.logger`)

Controls logging behavior and log collection.

Default values:

- `log_folder`: `"logs"`
- `intercept_selenium_logs`: `True`
- `intercept_playwright_logs`: `True`
- `intercept_appium_logs`: `True`

Example:

```python
config.logger.log_folder = "logs"
config.logger.intercept_selenium_logs = True
```

---

## Page Object configuration (`config.page_object`)

Controls Page Object execution behavior, retries, logging, and viewport breakpoints.

### Execution and logging

- `start_retries`: number of retry cycles per node (default: `3`)
- `retry_delay`: delay between retries (default: `1`)
- `post_morten_dumps`: enable post-mortem dumps on failure
- `auto_quit`: automatically quit drivers after execution
- `log_private`: include private Page Object methods in logs

### Viewport breakpoints (responsive design)

- `viewport_xs`: `0`
- `viewport_sm`: `576`
- `viewport_md`: `768`
- `viewport_lg`: `992`
- `viewport_xl`: `1200`
- `viewport_xxl`: `1400`

These values define breakpoint thresholds used for **responsive locator resolution**.

### Default viewport resolutions

- `default_xs_resolution`: `"375x667"`
- `default_sm_resolution`: `"600x1000"`
- `default_md_resolution`: `"768x1024"`
- `default_lg_resolution`: `"1280x800"`
- `default_xl_resolution`: `"1536x9607"`
- `default_xxl_resolution`: `"2560x1440"`

These values are used as practical defaults for responsive testing scenarios.

---

## Element configuration (`config.element`)

Controls element lookup, waiting, and stale recovery behavior.

Default values:

- `search_attempts`: `3`
- `search_retry_timeout`: `0.5`
- `stale_recovery_timeout`: `0.5`
- `wait_timeout`: `30`
- `missing_timeout`: `5`

These values define **framework-level synchronization behavior** and are applied automatically.

---

## Web capabilities (`config.web_capabilities`)

Controls browser automation capabilities.

Default values:

- `automation`: `"selenium"`
- `browser`: OS-dependent default (`edge`, `firefox`, `safari`, or `chrome`)
- `headless`: `True`

Capabilities are merged with user-provided values at runtime.

---

## Mobile capabilities (`config.mobile_capabilities`)

Controls mobile automation capabilities.

Default values:

- `automation`: `"appium"`
- `automation_name`: `"XCUITest"`
- `platform_name`: `"iOS"`
- `device_name`: `"iPhone 14"`
- `platform_version`: `"16.2"`
- `auto_accept_alerts`: `False`
- `new_command_timeout`: `300`

---

## Desktop capabilities (`config.desktop_capabilities`)

Controls desktop automation capabilities.

Default values:

- `automation`: `"appium"`
- `automation_name`: `"Mac"`
- `platform_name`: `"Mac"`
- `device_name`: `"Mac"`
- `platform_version`: `""`
- `new_command_timeout`: `300`

---

## REST configuration (`config.rest`)

Controls REST/HTTP client behavior.

Default values:

- `follow_redirects`: `True`
- `post_redirect_get`: `False`
- `accept_errors`: `False`
- `redirections_limit`: `20`
- `connection_timeout`: `10`
- `request_timeout`: `30`
- `log_redirects`: `False`

---

## Visual testing configuration (`config.visual`)

Controls visual comparison behavior.

Default values:

- `mode`: visual comparison mode
- `default_mismatch_threshold`: `5.0`
- `default_partial_mismatch_threshold`: `0.5`

---

## CLI configuration (`config.cli`)

Controls CLI execution and orchestration behavior.

Default values:

- `execution_timeout`: `60`
- `wait_idle_time`: `1`
- `command_registration_time`: `0.3`
- `ssh_connection_explicit_wait`: `1`

---

## Capabilities merging behavior

Capability sections (`web_capabilities`, `mobile_capabilities`, `desktop_capabilities`)
support merging with user-provided capability dictionaries.

Guarantees:

- framework defaults are applied first
- user-provided values override defaults
- keys may be transformed to camelCase when required by the backend

This behavior is internal to the framework and requires no special handling by tests.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Visual Testing API](/docs/reference/public-api/visual.md)  
→ Next: [Exceptions](/docs/reference/public-api/exceptions.md)