← [Back to Documentation Index](/docs/index.md)  
← Previous: [Project Setup (pytest)](/docs/getting-started/project-setup-pytest.md)  
→ Next: [Quickstart: Web UI Testing](/docs/getting-started/quickstart-web.md)

---

# 1.3 Basic Configuration

Hyperion is designed so that **configuration is optional**.

You can start writing and running tests immediately using built-in defaults.  
Configuration is only needed when you want to customize behavior.

This section explains:
- how configuration is discovered and loaded
- where configuration files can live
- how environment variables override configuration
- how to override configuration at runtime

---

## Configuration access

All configuration is exposed through the global `config` object:

```python
from hyperiontf import config
```

You never need to instantiate or initialize configuration manually.

---

## Automatic configuration loading

On first access, Hyperion automatically attempts to load a default configuration file  
**if one exists**.

### Lookup locations (in order)

1. Project working directory (`PWD`)
2. `PWD/config/`

### Supported filenames

The first matching file is loaded:

- `hyperion.ini`
- `hyperion.conf`
- `hyperion.cfg`
- `hyperion.json`
- `hyperion.yml`
- `hyperion.yaml`

If no configuration file is found, Hyperion continues using default values.

No error is raised.

---

## Configuration formats

Hyperion supports multiple configuration formats:

- **INI / CONF / CFG** — parsed using `configparser`
- **JSON**
- **YAML**

All formats map to the same internal configuration model.

---

## Environment variable overrides

Environment variables have **higher precedence** than configuration files.

This is especially useful for CI pipelines and containerized environments.

Currently supported environment variables:

- `HYPERION_LOG_FOLDER` → `config.logger.log_folder`
- `HYPERION_VISUAL_MODE` → `config.visual.mode`

If an environment variable is set, it overrides the value from any configuration file.

---

## Runtime configuration overrides

Explicit runtime assignments always have the **highest priority**.

```python
from hyperiontf import config

config.logger.log_folder = "custom_logs"
```

Runtime overrides replace:
- environment variable values
- configuration file values
- defaults

---

## Logging configuration

Logging is enabled by default.

You may configure the log output directory:

```python
from hyperiontf import config

config.logger.log_folder = "logs"
```

Behavior:
- the directory is created automatically if it does not exist
- relative paths are resolved against the project working directory
- absolute paths and `~/` paths are respected as-is

---

## Visual testing mode

Visual testing supports two modes:

- `compare` (default)
- `collect`

You can control the mode via environment variable:

```bash
export HYPERION_VISUAL_MODE=collect
```

Or at runtime:

```python
from hyperiontf import config

config.visual.mode = "collect"
```

---

## Capabilities overview

Capabilities define how automation tools are started.

They are configured via dedicated sections such as:

- `web_capabilities`
- `mobile_capabilities`
- `desktop_capabilities`

Only values you explicitly set are overridden; all others use defaults.

Example (Selenium):

```python
from hyperiontf import config

config.web_capabilities.automation = "selenium"
config.web_capabilities.browser = "chrome"
config.web_capabilities.headless = True
```

---

## Summary

- Configuration is optional
- Defaults are safe and intentional
- Configuration files are loaded automatically if present
- Environment variables override configuration files
- Runtime assignments override everything

With configuration in place (or not), you are ready to start writing tests.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Project Setup (pytest)](/docs/getting-started/project-setup-pytest.md)  
→ Next: [Quickstart: Web UI Testing](/docs/getting-started/quickstart-web.md)