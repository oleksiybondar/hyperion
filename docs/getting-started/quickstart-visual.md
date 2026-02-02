← [Back to Documentation Index](/docs/index.md)  
→ Next: [Hyperion Page Object Model (POM)](/docs/core-concepts/pom.md)

---

# 1.7 Quickstart: Visual Testing

This Quickstart shows a minimal, end-to-end example of **visual testing** in Hyperion.

Visual testing allows you to assert that:
- a page still looks the same
- a specific UI element has not visually changed

Hyperion supports visual assertions at both **page** and **element** level, with two modes:
- **COLLECT** — capture a baseline image
- **COMPARE** — compare against an existing baseline

---

## Minimal setup

This example assumes you already completed:

- [1.1 Installation](/docs/getting-started/installation.md)
- [1.2 Project Setup (pytest)](/docs/getting-started/project-setup-pytest.md)
- [1.3 Basic Configuration](/docs/getting-started/configuration.md)

No additional setup is required to use visual assertions.

---

## Page Object

Visual assertions are executed on existing page objects or elements.  
No special base classes or decorators are required beyond normal UI testing.

In this example, we reuse a simple page with a header element.

```python
from hyperiontf import WebPage, By, element


class DashboardPage(WebPage):
    """
    Example page used for visual assertions.
    """

    @element
    def header(self):
        return By.css("header.main-header")
```

---

## The test

This single test demonstrates:
- **Page-level visual assertion**
- **Element-level visual assertion**
- Switching between **COLLECT** and **COMPARE** modes

In practice, baseline collection is usually done once (or explicitly), and comparisons run on every test execution.

```python
import pytest
from hyperiontf import VisualMode
from hyperiontf import expect


@pytest.fixture(scope="function")
def dashboard_page():
    page = DashboardPage.start_browser("chrome")
    page.open("https://example.test/dashboard")
    yield page
    page.quit()


def test_dashboard_visuals(dashboard_page):
    # --- Page-level visual check ---
    # Collect a baseline or compare against an existing one.
    dashboard_page.verify_visual_match(
        name="dashboard-page",
        mode=VisualMode.COLLECT,
        mismatch_threshold=0,
    )

    # --- Element-level visual check ---
    # Element visuals can be asserted independently.
    dashboard_page.header.verify_visual_match(
        name="dashboard-header",
        mode=VisualMode.COLLECT,
        mismatch_threshold=0,
    )

    # In normal test runs, you would switch to COMPARE mode:
    #
    # dashboard_page.verify_visual_match(
    #     name="dashboard-page",
    #     mode=VisualMode.COMPARE,
    #     mismatch_threshold=2,
    # )
    #
    # dashboard_page.header.verify_visual_match(
    #     name="dashboard-header",
    #     mode=VisualMode.COMPARE,
    #     mismatch_threshold=2,
    # )
```

---

## What just happened

- You performed a visual assertion on the **entire page**.
- You performed a visual assertion on a **specific element**.
- Baseline collection and comparison are controlled explicitly via `VisualMode`.
- A mismatch threshold defines how much visual difference is allowed.

---

## What this already demonstrates

Without additional configuration, this Quickstart exercised:

- Page-level visual testing
- Element-level visual testing
- Explicit baseline collection vs comparison
- Threshold-based visual comparison
- Visual assertions integrated directly into Page Objects

---

← [Back to Documentation Index](/docs/index.md)  
→ Next: [Hyperion Page Object Model (POM)](/docs/core-concepts/pom.md)