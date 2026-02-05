← [Back to Documentation Index](/docs/index.md)  
← Previous: [Cross-Platform Calculator Example](/docs/examples/patterns/cross-platform-calculator.md)  
→ Next: [Page Object Layout Patterns](/docs/examples/patterns/page-object-layouts.md)

---

# 7.3 Page Object Layout Patterns

This section describes **how to structure Page Objects at scale** so they remain:

- readable
- reusable
- stable across UI changes
- consistent across platforms and teams

If **7.1** showed *what reuse looks like* and **7.2** explained *how to design widgets*,  
this section explains **how to assemble everything into a maintainable Page Object layout**.

---

## Think in layers, not files

A common mistake is to think about Page Objects as files or classes first.

Instead, think in **layers of responsibility**:

1. **Tests**  
   Express intent and assert outcomes.

2. **Page Objects**  
   Orchestrate behavior across widgets and elements.

3. **Widgets**  
   Encapsulate UI components and their internal variability.

4. **Elements**  
   Represent individual, resolved UI targets.

Good layout keeps each layer focused on *one level of abstraction*.

---

## Align Page Objects with UI structure

Modern applications already have structure:

- application shell
- feature areas
- reusable components
- repeated UI patterns

Your Page Object layout should mirror this structure.

Typical mapping:

- application / screen → Page Object
- feature area / section → Widget
- repeated UI component → Widget
- atomic control → Element (inside a widget or page)

This alignment makes the test code intuitive even for people who did not write it.

---

## Pattern: contract-first base class + thin platform types

The primary reuse pattern in Hyperion is:

- one **contract-focused Page Object**
- multiple **platform-specific entry points**

```python
class Calculator:
    @element
    def result(self):
        return {
            "web": By.id("<web result>"),
            "mobile": {"Android": By.id("<android result>")},
            "desktop": {"Darwin": By.predicate("<mac predicate>")},
        }

    @widget(klass=Keypad)
    def keypad(self):
        pass

    def evaluate_expression(self, a: float, op: str, b: float) -> None:
        self.keypad.evaluate_expression(a, op, b)


class WebCalculator(WebPage, Calculator):
    pass

class MobileCalculator(MobileScreen, Calculator):
    pass

class DesktopCalculator(DesktopWindow, Calculator):
    pass
```

Why this layout works:

- behavior is defined once
- locator variability is declared once
- platform classes stay thin and predictable
- tests choose platform by choosing the Page Object type

---

## Pattern: composition over inheritance for features

Inheritance is useful for **platform selection**, but it scales poorly for features.

Avoid deep inheritance trees like:

> `BasePage → AuthPage → DashboardPage → AdminDashboardPage`

Instead, model features as **widgets** and compose them into Page Objects.

```python
class Dashboard(WebPage):
    @widget(klass=Header)
    def header(self):
        pass

    @widget(klass=ResultsTable)
    def results(self):
        pass

    def search(self, query: str) -> None:
        self.header.search(query)
        self.results.wait_for_rows()
```

This keeps:

- widgets reusable
- Page Objects readable
- behavior localized

---

## Pattern: Page Objects orchestrate, widgets execute

A useful mental rule:

> **Page Objects coordinate; widgets do the work.**

Page Object methods typically:

- combine multiple widget actions
- express user-level workflows
- hide sequencing and timing

Widgets typically:

- interact with elements
- contain locator variability
- wait for observable UI state

This separation keeps both layers clean.

---

## Pattern: navigation is explicit, interaction is focused

Pages often mix two concerns:

1. *How do I get here?*  
2. *What can I do once I’m here?*

Keep navigation entry points obvious and limited:

- `open(...)`
- `open_url(...)`
- `go_to_<feature>()`

Then keep interaction methods focused on **behavior**, not routing.

This avoids Page Objects becoming navigation utilities instead of behavioral models.

---

## Pattern: isolate OS- and platform-specific logic at the lowest level

When behavior differs by platform or OS:

- prefer encoding it inside widgets
- otherwise encode it in the contract-level Page Object
- never push it into tests

This preserves the key guarantee shown in 7.1:

> Tests do not branch on platform.

For detailed rules, refer to:

- `/docs/how-to/os-specific-locators.md`
- `/docs/how-to/platform-agnostic-locators.md`

---

## Pattern: centralize shared flows, avoid “smart tests”

If multiple tests repeat the same multi-step interaction:

- extract it into a Page Object method **or**
- extract it into a shared flow that accepts a Page Object

```python
def calculator_flow(page) -> None:
    page.evaluate_expression(5.6, "+", 10.4)
    result = page.get_result()
    expect(result).to_be(16)
```

Tests stay short, expressive, and focused on intent.

---

## Pattern: structure by feature, not by technical role

As projects grow, feature-first layout scales better than role-first layout.

Prefer:

```python
page_objects/
  calculator/
    calculator.py
    keypad.py
  dashboard/
    dashboard.py
    header.py
    results_table.py
tests/
  calculator/
    test_calculator_web.py
    test_calculator_mobile.py
  dashboard/
    test_dashboard_smoke.py
```

This keeps related behavior close together and reduces cognitive load.

---

## Pattern: assertions live in tests, not in Page Objects

Page Objects should expose state in a stable, meaningful way:

- `page.total()`
- `table.row_count()`
- `header.error_message()`

Tests make the final claim:

- `expect(page.total()).to_be(...)`
- `assert table.row_count() > 0`

Page Objects provide *information*; tests decide *truth*.

---

## Pattern: never encode timing assumptions

Avoid:

- `time.sleep(...)`
- assumptions about load speed
- hidden retries in Page Object logic

Prefer:

- observable waits
- explicit readiness checks
- framework-provided retry semantics

This keeps Page Objects reliable across environments.

---

## How 7.1, 7.2, and 7.3 fit together

- **7.1** shows reuse in action (end-to-end)
- **7.2** explains how to design reusable widgets
- **7.3** explains how to assemble pages and widgets into scalable layouts

Together, they form a practical guide to writing cross-platform, maintainable Hyperion tests.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Cross-Platform Calculator Example](/docs/examples/patterns/cross-platform-calculator.md)  
→ Next: [Page Object Layout Patterns](/docs/examples/patterns/page-object-layouts.md)