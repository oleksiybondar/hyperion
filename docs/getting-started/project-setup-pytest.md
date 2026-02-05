← [Back to Documentation Index](/docs/index.md)  
← Previous: [Installation](/docs/getting-started/installation.md)  
→ Next: [Basic Configuration](/docs/getting-started/configuration.md)

---

# 1.2 Project Setup (pytest)

Hyperion is designed to work **with pytest**, not replace it.

If you already use pytest, you do **not** need to change how:
- tests are discovered
- tests are executed
- markers are defined
- fixtures are structured

Hyperion layers additional behavior (mainly logging and lifecycle helpers) on top of standard pytest constructs.

---

## Using pytest with Hyperion

Hyperion does not introduce a custom test runner.

You run your tests exactly as you would in any pytest project:

- `pytest`
- `pytest -k my_test`
- `pytest -m smoke`
- `pytest path/to/tests`

Test discovery, ordering, filtering, and execution semantics remain **pure pytest**.

---

## Required pytest integration import

Hyperion provides an **auto-invoked pytest fixture** named `hyperion_test_case_setup`.

This fixture is activated simply by importing it:

```python
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401
```

Important points:

- The fixture is used for **side effects only**
- It does **not** need to be referenced in test code
- The `# noqa: F401` comment is intentional
- Importing it once (for example in `conftest.py`) is sufficient

This fixture integrates pytest’s test lifecycle with Hyperion’s logging and execution context.

---

## The Hyperion fixture

Hyperion also provides its own `fixture` decorator, which is a **thin wrapper around a standard pytest fixture**.

The wrapped fixture:
- behaves exactly like a normal pytest fixture
- adds automatic logging context management
- requires no special teardown logic

Internally, the wrapper pushes and pops a log folder around the fixture lifecycle, but this does not change how pytest treats the fixture.

### Example fixture

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401
from hyperiontf.executors.pytest import fixture
from my_project.pages import HomePage


@fixture(scope="function")
def home_page():
    page = HomePage.start_browser("chrome")
    page.open("https://example.test")
    yield page
    page.quit()
```

Aside from the decorator import, this is a **regular pytest fixture**.

---

## Automatic logging initialization

Hyperion logging is initialized automatically.

In most projects, this is done simply by **importing the logging configurator** somewhere in your test setup (for example, in `conftest.py`).

No explicit “start logging” call is required.

This is intentional: Hyperion assumes logging is always enabled so that test execution is fully observable by default.

---

## Test metadata in logs

Hyperion enriches test logs using existing pytest metadata.

Specifically:

- **Test docstrings** are copied into the HTML log as the test header
- **Pytest markers** are captured and reflected in the log output

This means you can document and categorize tests using standard pytest mechanisms, and that information will automatically appear in Hyperion’s reports.

### Example test

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401


@pytest.mark.checkout
@pytest.mark.critical
def test_payment_flow():
    """
    Verifies that a user can complete a payment successfully.
    """
    ...
```

In this example:
- The docstring becomes the test description in the log
- The `checkout` and `critical` markers are visible in the report

---

## What Hyperion does *not* change

It is important to understand what remains untouched.

Hyperion does **not**:
- modify pytest’s execution model
- replace pytest fixtures
- override pytest markers
- introduce a custom test runner
- interfere with pytest CLI options

Everything outside of Hyperion’s explicit APIs behaves exactly as standard pytest.

---

## Summary

When setting up a project with pytest and Hyperion:

- Use pytest normally
- Import `hyperion_test_case_setup` once
- Use Hyperion’s `fixture` decorator where logging context is needed
- Let logging initialize automatically
- Write tests and docstrings as usual

Hyperion augments pytest with structure and observability, while keeping the underlying testing model familiar and predictable.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Installation](/docs/getting-started/installation.md)  
→ Next: [Basic Configuration](/docs/getting-started/configuration.md)
