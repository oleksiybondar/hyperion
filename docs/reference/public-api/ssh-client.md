← [CLI Client](/docs/reference/public-api/cli-client.md) | [Visual Testing API →](/docs/reference/public-api/visual.md)

# SSHClient

`SSHClient` is Hyperion’s public client for interacting with remote machines over **SSH** through a **persistent interactive session**.

You can:
- run **non-interactive** commands (`execute`)
- run **interactive** remote workflows (`exec_interactive` + `send_keys`)
- **wait** by observing remote output (`wait`) instead of sleeping
- inspect cached **output**
- **verify** decisions (logs + result object) with `verify_*`
- **assert** outcomes with `assert_*`

`SSHClient` inherits its interaction API from `BaseShell`. The methods listed below are the public surface you use in tests.

---

## Import

```python
from hyperiontf import SSHClient
```

---

## Lifecycle

An `SSHClient` establishes a real SSH session on creation and keeps it alive until `quit()` is called.

Typical test structure:
- create `SSHClient(...)`
- run commands and make decisions with `verify_*` when needed
- end the test with explicit `assert_*`
- call `quit()` in teardown

```python
from hyperiontf import SSHClient

def test_ssh_example():
    ssh = SSHClient(host="example.org", user="tester", password="secret")
    try:
        ssh.execute('echo "Hello from SSH"')
        ssh.assert_output_contains("Hello from SSH")
        ssh.assert_exit_code(0)
    finally:
        ssh.quit()
```

---

## Constructor

### `SSHClient(host, user, password=None, private_key=None, port=22)`

**Signature**
- `SSHClient(host: str, user: str, password: str | None = None, private_key: str | None = None, port: int = 22) -> SSHClient`

**Description**
Creates an SSH client and starts a **persistent interactive SSH session** immediately.

Authentication rules:
- If `private_key` is provided, key-based authentication is used.
- Otherwise, password-based authentication is used.

**Arguments**
- `host: str`  
  Remote host to connect to (hostname or IP).
- `user: str`  
  Username for authentication.
- `password: str | None`  
  Password for authentication (used when `private_key` is not provided).
- `private_key: str | None`  
  Path to a private key file for key-based authentication.
- `port: int`  
  SSH port. Default: `22`.

**Returns**
- `SSHClient`

**Raises**
- `CommandExecutionException` if the SSH connection or session cannot be established.

---

## Output access

### `output`

**Signature**
- `output -> str`

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
- `execute(command: str, timeout: int | None = config.cli.execution_timeout) -> None`

**Description**
Executes a **non-interactive** command on the remote session and waits until the command completes.

On completion:
- output produced by the command is cached and available via `output`
- the exit code of the last command is recorded (and can be asserted with `assert_exit_code(...)`)

**Arguments**
- `command: str`  
  Command to execute remotely.
- `timeout: int | None`  
  Maximum time to wait for completion.

**Returns**
- `None`

**Raises**
- `CommandExecutionTimeoutException` if completion is not detected within `timeout`.

---

### `exec_interactive(command)`

**Signature**
- `exec_interactive(command: str) -> None`

**Description**
Starts an **interactive** remote command (one that expects follow-up input). Use `wait(...)` to observe prompts and `send_keys(...)` to respond.

**Arguments**
- `command: str`  
  Interactive command to start.

**Returns**
- `None`

---

### `send_keys(data)`

**Signature**
- `send_keys(data: str) -> None`

**Description**
Sends interactive input to the remote session.

**Arguments**
- `data: str`  
  Input to send.

**Returns**
- `None`

---

## Waiting and reading output

### `wait(pattern=None, timeout=config.cli.execution_timeout)`

**Signature**
- `wait(pattern: str | None = None, timeout: int = config.cli.execution_timeout) -> None`

**Description**
Waits until remote output indicates progress:
- If `pattern` is provided: waits until the session output ends with that `pattern`.
- If `pattern` is `None`: waits until the session returns to its “ready” prompt state.

This is **interactive waiting**: you wait on observable output, not time.

**Arguments**
- `pattern: str | None`  
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
Performs an immediate, non-blocking read of any currently available output and appends it to the internal cache.

Unlike `wait(...)`, it does not wait for a prompt or pattern — it simply collects whatever output is available at the moment of the call.

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
Closes the interactive remote session and releases resources. Always call this in teardown.

**Returns**
- `None`

---

## Example: key-based authentication

```python
from hyperiontf import SSHClient

def test_ssh_with_key():
    ssh = SSHClient(
        host="example.org",
        user="tester",
        private_key="/home/tester/.ssh/id_rsa",
        port=22,
    )
    try:
        ssh.execute("whoami")
        ssh.assert_output_contains("tester")
        ssh.assert_exit_code(0)
    finally:
        ssh.quit()
```

---

## Example: interactive waiting (no sleeps)

```
from hyperiontf import SSHClient

def test_ssh_interactive():
    ssh = SSHClient(host="example.org", user="tester", password="secret")
    try:
        ssh.exec_interactive('read -p "Enter value: " v; echo $v')

        ssh.wait("Enter value:")
        ssh.send_keys("Hyperion")
        ssh.wait()

        ssh.assert_output_contains("Hyperion")
        ssh.assert_exit_code(0)
    finally:
        ssh.quit()
```

---

← [CLI Client](/docs/reference/public-api/cli-client.md) | [Visual Testing API →](/docs/reference/public-api/visual.md)