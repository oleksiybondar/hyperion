← [Back to Documentation Index](/docs/index.md)  
← Previous: [Exceptions](/docs/reference/public-api/exceptions.md)  
→ Next: [Locator Resolution Order](/docs/reference/behavior-contracts/locator-resolution.md)

---

# 5.20 Logger

Hyperion provides a custom logger that extends Python’s standard `logging.Logger` with **test-log oriented capabilities**.

The Hyperion logger is designed to support:

- **per-test log files**
- **hierarchical log grouping** (expand / collapse in HTML logs)
- **merging external logger output** into the same test log stream

Hyperion uses this logger internally for Page Objects, fixtures, and test execution.
You may also use it directly when you want to add **high-level structure** to your test logs.

---

## Import

```python
from hyperiontf.logging import getLogger, Logger
```

---

## getLogger

### `getLogger(name: str = "TestCase") -> Logger`

Returns a Hyperion `Logger` instance with the given name.

- If a logger with the same name already exists, it is returned.
- The returned object is Hyperion’s custom `Logger`, not a standard `logging.Logger`.

#### Arguments

- `name`: logger name (defaults to `"TestCase"`)

#### Returns

- `Logger`: Hyperion logger instance

#### Example

```python
from hyperiontf.logging import getLogger

logger = getLogger("MySuite")
logger.info("Suite started")
```

---

## Logger

`Logger` extends `logging.Logger` and adds a minimal set of APIs used by Hyperion’s logging model.

You normally do **not** instantiate `Logger` directly.  
Always obtain it via `getLogger(...)`.

---

## Folder (depth) control

Folder depth controls how log records are grouped in the HTML log output.

This allows complex flows to be displayed as **collapsible sections**, making logs easier to read and navigate.

---

### `push_folder(message: str | None = None) -> None`

Opens a new logical log group (“folder”) by increasing the current log depth.

If `message` is provided, it is logged at the new depth.

#### Arguments

- `message`: optional message to log when entering the folder

#### Example

```python
from hyperiontf.logging import getLogger

logger = getLogger("TestCase")

logger.push_folder("Checkout flow")
logger.info("Selecting shipping method")
logger.info("Submitting payment")
logger.pop_folder()
```

---

### `pop_folder() -> None`

Closes the most recently opened folder by decreasing the log depth.

This also emits an end-of-folder marker so the HTML log renderer can properly close the section.

---

### `pop_all() -> None`

Closes **all** open folders and resets log depth back to zero.

This is useful as a cleanup operation when a flow exits early or raises an exception.

---

## Log file initialization

Hyperion’s pytest integration typically initializes a per-test log file automatically.

These APIs are available if you need explicit control.

---

### `init_test_log(test_name: str) -> None`

Initializes a test-specific log file using `test_name` to derive the filename.

#### Arguments

- `test_name`: test name used for log file generation

---

### `init_log_file(new_name: str) -> None`

Initializes or switches logging output to a specific log file.

#### Arguments

- `new_name`: file name (or relative path) to use for logging output

---

## Merging external logger streams

### `merge_logger_stream(name: str) -> None`

Merges another named Python logger into the same Hyperion log output stream.

This allows output from third-party libraries (that use their own loggers) to appear inside the same test log file and HTML report.

#### Arguments

- `name`: name of the other logger to merge

#### Example

```python
import logging
from hyperiontf.logging import getLogger

logger = getLogger("TestCase")

logger.merge_logger_stream("some.library")

external_logger = logging.getLogger("some.library")
external_logger.info("This message appears in the Hyperion test log")
```

---

## Usage guidance

- You usually **do not need to call the logger directly** in normal test code.
- Page Object methods, expectations, retries, and context switching are logged automatically.
- Use `push_folder(...)` sparingly to group **high-level logical steps**, not individual actions.
- Avoid using the logger for assertions; assertions should remain in test logic.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Exceptions](/docs/reference/public-api/exceptions.md)  
→ Next: [Locator Resolution Order](/docs/reference/behavior-contracts/locator-resolution.md)
