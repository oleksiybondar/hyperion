← [Back to Documentation Index](/docs/index.md)  
← Previous: [CLI Testing](/docs/how-to/cli-testing-cli-client.md)  
→ Next: [Visual Testing and Baselines](/docs/how-to/visual-testing-baselines.md)

---

# SSH Testing with `SSHClient`

This guide shows practical patterns for validating remote systems using Hyperion’s `SSHClient`.

It focuses on:
- stable session lifecycle (fixtures + finalizers)
- interactive waiting (no sleeps)
- optional “sudo priming” for repeatable privileged commands
- realistic examples (system checks and service validation)

---

## Guiding principles

- Prefer **fixture-based lifecycle management**
- Prefer **interactive waiting** (`wait(...)`) over sleeping
- Use `verify_*` only for **decision logging**
- Tests must **always end with explicit `assert_*`**
- Avoid inline cleanup logic inside tests whenever possible

> ⚠️ `try / finally` inside tests is **discouraged**  
> It may introduce flakiness or false-positives by masking failures.  
> Use it **only** in exceptional cases where fixtures cannot model the lifecycle
> (for example: concurrency tests that keep multiple sessions open).

---

## Mandatory imports (pytest + Hyperion logging)

Every SSH test module **must** include these imports:

- `pytest` — required by pytest even if not referenced directly
- `hyperion_test_case_setup` — auto-invoked fixture that ensures:
  - a **separate structured log file per test**
  - correct Hyperion logging lifecycle

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401

from hyperiontf import SSHClient, expect
from hyperiontf.executors.pytest import fixture
```

---

## Recommended lifecycle pattern (fixture + finalizer)

The recommended approach is to create one SSH session per test and clean it up via a finalizer.

```python
@fixture(autouse=True, log=False)
def ssh_client(request):
    client = SSHClient(host="example-host", user="tester", password="secret")
    request.addfinalizer(client.quit)
    yield client
```

> Tip: keep connection details in your own constants/config, but keep test code focused on behavior.

---

## Optional: sudo session priming (interactive, once)

If your checks frequently use `sudo`, priming the sudo session once in the fixture makes tests:
- faster (no repeated prompts)
- more deterministic (no surprise interactive password requests)
- easier to read (tests stay non-interactive)

This uses an interactive step:
- start `sudo` command
- wait for the exact password prompt
- send the password
- wait for the session to return to the action prompt
- flush leftover output

```python
@fixture(autouse=True, log=False)
def ssh_client(request):
    password = "secret"
    client = SSHClient(host="example-host", user="tester", password=password)
    request.addfinalizer(client.quit)

    # Prime sudo session once per test
    client.exec_interactive("sudo whoami")
    client.wait("[sudo] password for tester:")
    client.send_keys(password)

    # Wait until the session is ready again
    client.wait(client.action_prompt)

    # Clear any leftover output so later assertions are stable
    client.flush_output()

    yield client
```

Notes:
- The prompt text varies by OS configuration. Always wait for the exact string your system prints.
- If you don’t need sudo in your suite, skip this step and keep the fixture minimal.

---

## Running remote commands

Use `execute(...)` for non-interactive commands.

```python
def test_cpu_supports_virtualization(ssh_client):
    ssh_client.execute(r"grep -E 'vmx|svm' /proc/cpuinfo >/dev/null 2>&1")
    ssh_client.assert_exit_code(0)
```

For output parsing, use plain Python and `expect(...)`:

```python
def test_kvm_modules_loaded(ssh_client):
    ssh_client.execute("lsmod | awk '{print $1}' | grep -E '^kvm(_intel|_amd)?$' -o | sort -u")
    mods = {m.strip() for m in ssh_client.output.splitlines() if m.strip()}

    expect(mods).to_contain("kvm")
    expect(bool({"kvm_intel", "kvm_amd"} & mods)).to_be(True)

    ssh_client.assert_exit_code(0)
```

---

## Systemd validation example (services and one-shots)

### Pattern: required services are active

```python
def test_required_services_active(ssh_client):
    required = [
        "service-a.service",
        "service-b.service",
    ]

    for unit in required:
        ssh_client.execute(f"sudo systemctl is-active {unit}")
        ssh_client.assert_output("active")
```

### Pattern: one-shot services exist and are not failed

One-shot services may show as “exited” and still be healthy.
A stable approach is to request a small, deterministic set of properties.

```python
def test_required_oneshots_not_failed(ssh_client):
    oneshots = [
        "oneshot-a.service",
        "oneshot-b.service",
    ]

    for unit in oneshots:
        ssh_client.execute(
            "TERM=dumb SYSTEMD_COLORS=0 "
            f"sudo systemctl show {unit} -p ActiveState -p SubState -p ExecMainStatus"
        )
        ssh_client.assert_output("ExecMainStatus=0\nActiveState=active\nSubState=exited")
```

---

## Writing small helpers (recommended)

Helpers keep tests readable and reduce duplication.

```python
def cmd_exists(ssh: SSHClient, cmd: str) -> bool:
    ssh.execute(f"command -v {cmd}")
    return ssh.exit_code == 0

def systemd_is_active_or_missing(ssh: SSHClient, unit: str) -> bool:
    ssh.execute(f"sudo systemctl is-active {unit} || true")
    return "active" in ssh.output
```

---

## `verify_*` vs `assert_*`

Use `verify_*` only for **decision logging**, then end the test with `assert_*`.

```python
def test_decision_logging(ssh_client):
    ssh_client.execute("uname -r")

    ssh_client.verify_output_contains(".")
    ssh_client.assert_exit_code(0)
```

---

## Exceptional case: concurrency testing (multiple sessions)

Some scenarios require holding multiple sessions open simultaneously.
This is one of the few cases where inline cleanup is hard to avoid.

```python
def test_max_concurrent_ssh_sessions():
    max_allowed = 5
    clients = []

    try:
        for _ in range(max_allowed):
            c = SSHClient(host="example-host", user="tester", password="secret")
            c.execute("whoami")
            c.assert_exit_code(0)
            c.assert_output("tester")
            clients.append(c)

        with pytest.raises(Exception):
            extra = SSHClient(host="example-host", user="tester", password="secret")
            extra.execute("echo should_not_succeed")
            extra.quit()
    finally:
        for c in clients:
            try:
                c.quit()
            except Exception:
                pass
```

---

## Common pitfalls

- ❌ Sleeping instead of waiting  
  → use `wait(...)` with observable patterns
- ❌ Forgetting to prime sudo but running privileged commands  
  → either prime sudo once, or keep commands non-sudo
- ❌ Treating `verify_*` as a soft assertion  
  → tests must end with explicit `assert_*`
- ❌ Inline cleanup as default  
  → prefer fixtures with `request.addfinalizer(...)`

---

## Summary

**Default**
- fixture + finalizer per test
- optional sudo priming in fixture (if needed)
- interactive waiting
- explicit assertions

**Exceptional**
- inline multi-client cleanup only when fixtures cannot model the lifecycle (e.g., concurrency tests)

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [CLI Testing](/docs/how-to/cli-testing-cli-client.md)  
→ Next: [Visual Testing and Baselines](/docs/how-to/visual-testing-baselines.md)
