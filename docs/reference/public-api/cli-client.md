← [Back to Documentation Index](/docs/index.md)  
← Previous: [REST Client](/docs/reference/public-api/http-client.md)  
→ Next: [SSH Client](/docs/reference/public-api/ssh-client.md)

---

# CLIClient

`CLIClient` is Hyperion’s public client for testing command-line programs through a **persistent shell session**.

You can:
- run **non-interactive** commands (`execute`)
- run **interactive** commands (`exec_interactive` + `send_keys`)
- **wait** by observing output (`wait`) instead of sleeping
- inspect cached **output**
- **verify** decisions (logs + result object) with `verify_*`
- **assert** outcomes with `assert_*`

`CLIClient` inherits its interaction API from `BaseShell`. The methods listed below are part of the public surface you use in tests.

---

## Import

```python
from hyperiontf import CLIClient
```

---

## Lifecycle

A `CLIClient` starts a real shell session on creation and keeps it alive until `quit()` is called.

Typical test structure:
- create `CLIClient(...)`
- run commands and make decisions with `verify_*` when needed
- end the test with explicit `assert_*`
- call `quit()` in teardown

```python
from hyperiontf import CLIClient

def test_cli_example():
    cli = CLIClient(shell="bash")
    try:
        cli.execute('echo "Hello"')
        cli.assert_output_contains("Hello")
        cli.assert_exit_code(0)
    finally:
        cli.quit()
```

---

## Constructor

### `CLIClient(shell="bash")`

**Signature**
- `CLIClient(shell: str = "bash") -> CLIClient`

**Description**
Creates a CLI client for the given shell and starts a **persistent session** immediately.

**Arguments**
- `shell: str`  
  Shell executable name. Supported values:
  - `"bash"`, `"sh"`, `"zsh"`, `"cmd"`, `"powershell"`

**Returns**
- `CLIClient`

**Raises**
- `CommandExecutionException` if the shell session cannot be started.

---

## Properties

### `shell`

**Signature**
- `shell -> str`

**Description**
Returns the configured shell name used as the session source identifier.

**Returns**
- `str`

---

### `output`

**Signature**
- `output() -> str`

**Description**
Returns the current cached output as a single string.

Output is accumulated into an internal cache as commands produce output. Most tests read `output` after:
- `execute(...)`
- `wait(...)`
- `read_output()`

**Returns**
- `str` (trimmed)

---

## Command execution

### `execute(command, timeout=config.cli.execution_timeout)`

**Signature**
- `execute(command: str, timeout: Optional[int] = config.cli.execution_timeout) -> None`

**Description**
Executes a **non-interactive** command and waits until the command completes (completion is detected by the session’s prompt behavior). The output produced by the command is cached and available via `output`.

**Arguments**
- `command: str`  
  Command to execute.
- `timeout: Optional[int]`  
  Maximum time to wait for completion.

**Returns**
- `None`

**Raises**
- `CommandExecutionTimeoutException` if completion is not detected within `timeout`.

---

### `exec_interactive(command)`

**Signature**
- `exec_interactive(command) -> None`

**Description**
Starts an **interactive** command (one that expects follow-up input). Use `wait(...)` to observe prompts and `send_keys(...)` to respond.

**Arguments**
- `command`  
  Interactive command to start.

**Returns**
- `None`

---

### `send_keys(data)`

**Signature**
- `send_keys(data: str) -> None`

**Description**
Sends interactive input to the active session.

**Arguments**
- `data: str`  
  Input to send.

**Returns**
- `None`

---

## Waiting and reading output

### `wait(pattern=None, timeout=config.cli.execution_timeout)`

**Signature**
- `wait(pattern: Optional[Union[str]] = None, timeout: int = config.cli.execution_timeout) -> None`

**Description**
Waits until session output indicates progress:
- If `pattern` is provided: waits until the session output ends with that `pattern`.
- If `pattern` is `None`: waits until the session returns to its “ready” prompt state.

This is **interactive waiting**: you wait on observable output, not time.

**Arguments**
- `pattern: Optional[str]`  
  Text to wait for at the end of output, or `None` to wait for the ready prompt.
- `timeout: int`  
  Maximum time to wait.

**Returns**
- `None`

**Raises**
- `CommandExecutionTimeoutException` if the condition is not met within `timeout`.

---

### `read_output()`

**Signature**
- `read_output() -> str`

**Description**
Performs an immediate, non-blocking read of any currently available output and appends it to the internal cache. Unlike `wait(...)`, it does not wait for a prompt or pattern.

**Returns**
- `str` (the full cached output after reading)

---

## Exit code checks

### `assert_exit_code(expected_code)`

**Signature**
- `assert_exit_code(expected_code: int) -> ExpectationResult`

**Description**
Asserts that the last recorded exit code matches `expected_code`.

Use this to end tests with an explicit assertion.

**Arguments**
- `expected_code: int`

**Returns**
- `ExpectationResult`

---

### `verify_exit_code(expected_code)`

**Signature**
- `verify_exit_code(expected_code: int) -> ExpectationResult`

**Description**
Logs a decision-style verification for the last recorded exit code without turning it into a test failure by itself.

Use `verify_*` when you want structured decision logging, then end the test with explicit `assert_*`.

**Arguments**
- `expected_code: int`

**Returns**
- `ExpectationResult`

---

## Output checks

### `assert_output(expected_output)`

**Signature**
- `assert_output(expected_output: str) -> ExpectationResult`

**Description**
Asserts that the current cached output is exactly `expected_output`.

**Arguments**
- `expected_output: str`

**Returns**
- `ExpectationResult`

---

### `verify_output(expected_output)`

**Signature**
- `verify_output(expected_output: str) -> ExpectationResult`

**Description**
Logs a decision-style verification that the current cached output is exactly `expected_output`.

**Arguments**
- `expected_output: str`

**Returns**
- `ExpectationResult`

---

### `assert_output_contains(expected_output)`

**Signature**
- `assert_output_contains(expected_output: str) -> ExpectationResult`

**Description**
Asserts that the current cached output contains `expected_output` as a substring.

**Arguments**
- `expected_output: str`

**Returns**
- `ExpectationResult`

---

### `verify_output_contains(expected_output)`

**Signature**
- `verify_output_contains(expected_output: str) -> ExpectationResult`

**Description**
Logs a decision-style verification that the current cached output contains `expected_output`.

**Arguments**
- `expected_output: str`

**Returns**
- `ExpectationResult`

---

## Session shutdown

### `quit()`

**Signature**
- `quit() -> None`

**Description**
Stops the persistent shell session and releases resources. Always call this in teardown.

**Returns**
- `None`

---

## Example: interactive waiting (no sleeps)

```python
from hyperiontf import CLIClient

def test_interactive_session():
    cli = CLIClient(shell="bash")
    try:
        cli.exec_interactive("python -q")

        # Wait for a prompt-like marker you expect from the tool/session.
        cli.wait(timeout=10)

        cli.send_keys("print(2 + 2)")
        cli.wait(timeout=10)

        cli.assert_output_contains("4")

        # End the test with explicit assertions
        cli.assert_exit_code(0)
    finally:
        cli.quit()
```

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [REST Client](/docs/reference/public-api/http-client.md)  
→ Next: [SSH Client](/docs/reference/public-api/ssh-client.md)
