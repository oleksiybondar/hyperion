← [REST API Testing](/docs/how-to/api-testing-rest-client.md) | [SSH Testing →](/docs/how-to/ssh-testing-ssh-client.md)

# CLI Testing with `CLIClient`

This guide documents **recommended, stable patterns** for testing command-line behavior using Hyperion’s `CLIClient`.

It is intentionally **how-to oriented**, not API-reference–style.

---

## Guiding principles

When testing CLI tools with Hyperion:

- Prefer **fixture-based lifecycle management**
- Prefer **interactive waiting** (`wait(...)`) over sleeping
- Use `verify_*` only for **decision logging**
- Tests must **always end with explicit `assert_*`**
- Avoid inline cleanup logic inside tests whenever possible

> ⚠️ `try / finally` inside tests is **discouraged**  
> It may introduce flakiness or false-positives by masking failures.  
> Use it **only** in exceptional cases where fixtures cannot model the lifecycle.

---

## Mandatory imports (pytest + Hyperion logging)

Every CLI test module **must** include these imports:

- `pytest` — required by pytest even if not referenced directly
- `hyperion_test_case_setup` — auto-invoked fixture that ensures:
  - a **separate structured log file per test**
  - correct Hyperion logging lifecycle

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401

from hyperiontf import CLIClient, expect
from hyperiontf.executors.pytest import fixture
```

> `hyperion_test_case_setup` appears unused by design.  
> It is auto-discovered and auto-invoked by pytest to prepare per-test logging.

---

## Recommended lifecycle pattern (fixture + finalizer)

The **default and recommended** way to manage a CLI session is via a pytest fixture with a finalizer.

This ensures:
- deterministic cleanup
- consistent behavior across failures
- no hidden control flow in tests

```python
from hyperiontf.executors.pytest import fixture
from hyperiontf import CLIClient

@fixture(autouse=True, log=False)
def cli_client(request):
    client = CLIClient(shell="bash")
    request.addfinalizer(client.quit)
    yield client
```

All examples below assume this fixture is in place.

---

## Running non-interactive commands

Use `execute(...)` for commands that complete on their own.

Assertions should be explicit and final.

```python
def test_simple_command(cli_client):
    cli_client.execute("echo Hello")

    cli_client.assert_output_contains("Hello")
    cli_client.assert_exit_code(0)
```

Parsing output is plain Python:

```python
def test_multiline_output(cli_client):
    cli_client.execute("printf 'a\nb\nc\n'")

    lines = [l.strip() for l in cli_client.output.splitlines() if l.strip()]
    expect(lines).to_contain("a")
    expect(lines).to_contain("b")
    expect(lines).to_contain("c")

    cli_client.assert_exit_code(0)
```

---

## Interactive CLI flows (no sleeps)

For interactive programs, coordinate progress using:
- `exec_interactive(...)`
- `wait(...)`
- `send_keys(...)`

Never rely on `time.sleep`.

```python
def test_interactive_python(cli_client):
    cli_client.exec_interactive("python -q")

    # Wait until the interpreter is ready
    cli_client.wait(timeout=10)

    cli_client.send_keys("print(2 + 2)")
    cli_client.wait(timeout=10)

    cli_client.assert_output_contains("4")
```

Guidelines:
- If the program emits a known prompt, pass it explicitly to `wait("prompt")`
- If output from a previous step should not affect later assertions, clear it
  (e.g. `flush_output()` if exposed by your client)

---

## `verify_*` vs `assert_*`

`verify_*` is for **decision logging**, not for determining test success.

Use it when:
- branching logic depends on runtime state
- you want structured logs without failing immediately

Always finish with `assert_*`.

```python
def test_decision_logging(cli_client):
    cli_client.execute("echo OK")

    # decision-style logging
    cli_client.verify_output_contains("OK")

    # explicit test outcome
    cli_client.assert_exit_code(0)
```

---

## Exceptional cases: dynamic or concurrent sessions

### ⚠️ Advanced pattern — use sparingly

In rare cases, fixtures cannot express the lifecycle correctly.

Examples:
- testing **maximum concurrent sessions**
- holding multiple sessions open simultaneously
- intentionally leaking a session until a failure occurs

In such cases, an inline `try / finally` may be unavoidable.

This is **an exception**, not a recommendation.

```python
def test_max_concurrent_cli_sessions():
    max_allowed = 5
    clients = []

    try:
        for _ in range(max_allowed):
            c = CLIClient(shell="bash")
            c.execute("echo session_alive")
            c.assert_exit_code(0)
            clients.append(c)

        # Attempt one more session — expected to fail
        with pytest.raises(Exception):
            extra = CLIClient(shell="bash")
            extra.execute("echo should_not_succeed")
            extra.quit()
    finally:
        for c in clients:
            try:
                c.quit()
            except Exception:
                pass
```

Notes:
- This pattern is intentionally explicit and defensive
- Cleanup is best-effort and must not mask the primary assertion
- Prefer fixtures whenever the lifecycle can be modeled declaratively

---

## Common pitfalls

- ❌ Sleeping instead of waiting  
  → use `wait(...)` with observable output
- ❌ Treating `verify_*` as a soft assertion  
  → tests must end with `assert_*`
- ❌ Inline cleanup as a default pattern  
  → prefer fixtures with `request.addfinalizer(...)`

---

## Summary

**Default**  
✔ fixture + finalizer  
✔ interactive waiting  
✔ explicit assertions  

**Exceptional**  
⚠️ inline `try / finally` only when fixtures cannot express the lifecycle

This keeps CLI tests:
- stable
- readable
- debuggable
- aligned with Hyperion’s execution model

---

← [REST API Testing](/docs/how-to/api-testing-rest-client.md) | [SSH Testing →](/docs/how-to/ssh-testing-ssh-client.md)