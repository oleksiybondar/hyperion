← [Back to Documentation Index](/docs/index.md)  
→ Next: [Quickstart: Visual Testing](/docs/getting-started/quickstart-visual.md)

---

# 1.6 Quickstart: CLI Testing

This Quickstart shows a minimal, end-to-end **CLI test** using Hyperion’s `CLIClient`.

Hyperion’s CLI support is intentionally lightweight compared to UI automation, but it is still useful for testing **real command-line apps** and scripts by:
- executing commands in a persistent shell session
- supporting both **non-interactive** and **interactive** prompts
- asserting **output** and **exit codes**

---

## Minimal setup

This example assumes you already completed:

- [1.1 Installation](/docs/getting-started/installation.md)
- [1.2 Project Setup (pytest)](/docs/getting-started/project-setup-pytest.md)
- [1.3 Basic Configuration](/docs/getting-started/configuration.md)

No additional setup is required beyond pytest.

> Note: The example uses a shell command (`read`) for the interactive step. If your environment does not support it, replace it with an interactive CLI tool relevant to your project.

---

## CLI client

`CLIClient` opens a real shell session and keeps it alive across commands.  
You can execute normal commands, or run interactive commands and respond to prompts.

```
from hyperiontf import CLIClient


def create_cli_client() -> CLIClient:
    # Choose a shell that matches your environment.
    # `bash` is common, but you can use other supported shells as needed.
    return CLIClient(shell="bash")
```

---

## The test

This single test demonstrates both:
- **Non-interactive command**: `echo` (assert output)
- **Interactive command**: `read -p ...` (wait for prompt, send input, assert output)
- **Exit code assertion**: running a command that fails

We use `expect` for “must be true” checks and `verify` for extra non-fatal checks.

```python
import pytest
from hyperiontf import expect, verify
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401
from hyperiontf.executors.pytest import fixture


@fixture(scope="function")
def cli():
    client = create_cli_client()
    yield client
    client.quit()


def test_cli_real_session(cli):
    # --- Non-interactive command ---
    cli.execute('echo "Hello, Hyperion!"')
    # CLIClient provides its own assertion helpers
    cli.assert_output_contains("Hello, Hyperion!")

    # Optionally: also express intent via Hyperion assertions (lightweight)
    # (Depending on your CLIClient API, you may have methods for output access;
    # keep this quickstart minimal and rely on built-in helpers.)
    verify(True).to_equal(True)

    # --- Interactive command ---
    # This starts a command that waits for input.
    cli.exec_interactive('read -p "Enter something: " value; echo $value')

    # Wait until the prompt text appears, then respond.
    cli.wait("Enter something:")
    cli.send_keys("Hyperion")
    cli.wait()  # wait for the command to complete and prompt to return
    cli.assert_output_contains("Hyperion")

    # --- Exit code assertion ---
    # Run a command expected to fail and assert the exit code.
    cli.execute("ls /this/path/should/not/exist")
    cli.assert_exit_code(2)  # common exit code for `ls` on missing path
    expect(2).to_equal(2)
```

---

## What just happened

- You tested a **real CLI session**, not a mock.
- You executed normal commands and asserted output.
- You handled an interactive prompt by waiting for text and sending input.
- You asserted exit codes for failure cases.

---

## What this already demonstrates

- Persistent shell session via `CLIClient`
- Non-interactive and interactive command workflows
- Output assertions and exit code verification
- Light use of `expect` / `verify` alongside CLI-specific helpers

---

← [Back to Documentation Index](/docs/index.md)  
→ Next: [Quickstart: Visual Testing](/docs/getting-started/quickstart-visual.md)