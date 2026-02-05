← [Back to Documentation Index](/docs/index.md)  
← Previous: [Reusable Widget Patterns](/docs/examples/patterns/reusable-widgets.md)  
→ Next: [High-Level Architecture Overview](/docs/architecture/overview.md)

---

# 7.2 Reusable Widget Patterns

Widgets are the primary unit of reuse in Hyperion.

If a Page Object describes a screen, page, or window at a **high level**, a widget represents a **self-contained UI component** with its own structure and behavior.

Common examples include:

- keypads / numeric panels
- navigation bars
- tables and lists
- filters and search panels
- modals and dialogs
- headers, footers, sidebars

Widgets help keep Page Objects small, expressive, and stable — especially in cross-platform and cross-OS scenarios.

---

## Think in UI components, not in elements

Modern web and mobile applications (React, Vue, native mobile UI frameworks) are already built from **components**.

Hyperion widgets intentionally map to that same idea.

If the application UI is already divided into components, you should usually mirror that structure in your Page Objects:

- a UI component → a widget
- repeated component → reusable widget
- composed components → widgets inside widgets

This alignment brings two benefits:

1. **Mental consistency**  
   Test structure matches how the UI is built and reasoned about.

2. **Natural reuse boundaries**  
   Changes in one component affect one widget, not the entire test suite.

---

## What makes a widget reusable

A reusable widget has three defining properties:

1. **A stable public interface**  
   Tests and Page Objects call widget methods (behavior), not locators.

2. **Internal structure hidden behind the interface**  
   Locators and element collections stay inside the widget.

3. **Locator variability handled inside the widget**  
   Platform-, OS-, or layout-specific differences are declared once and resolved at runtime.

In short: **tests should not care how the widget is implemented**.

---

## Heuristic: should this be a widget?

For less experienced users, deciding what deserves a widget can be difficult.

A simple rule of thumb:

> If **two or more** of the following are true, it should probably be a widget.

### Visual boundary
- The UI clearly looks like a component
- It has a visible container (panel, box, modal, section)

### Logical boundary
- It has a distinct responsibility or state
- It “owns” some data or behavior (filters, selection, pagination)

### Operational boundary
- It exposes meaningful actions  
  (for example: `search()`, `select_row()`, `apply_filter()`)

If none or only one applies, it may be better represented as a simple element inside a widget or page.

---

## Pattern: widget as a behavior boundary

Widget methods should represent **user intent**, not low-level interaction.

For example, a calculator widget does not “click a button”; it “presses a key”.

```python
class Keypad(Widget):
    def press(self, key: str) -> None:
        """Press a single key by label."""
        ...

    def evaluate_expression(self, a: float, op: str, b: float) -> None:
        """Enter and evaluate a full expression."""
        self.press(str(a))
        self.press(op)
        self.press(str(b))
        self.press("=")
```

Why this matters:

- Page Objects delegate behavior, not mechanics
- tests remain readable and intention-focused
- internal changes do not leak outward

---

## Pattern: default locator for the widget root

Many widgets have a clear root container.

Declaring a widget-level default locator means:

- Page Objects do not repeat locators
- all internal resolution is scoped to the widget context
- the widget can be embedded consistently across pages

```python
class Keypad(Widget):
    @property
    def default_locator(self):
        return {
            "web": By.css_selector("<web keypad root>"),
            "mobile": {"Android": By.id("<android keypad root>")},
            "desktop": {"Darwin": By.xpath("<mac keypad root>")},
        }
```

The values differ per platform or OS, but the contract does not.

---

## Pattern: element collections inside widgets

Many widgets are best expressed as a collection:

- buttons
- rows
- list items
- tabs

Declare the collection once and build behavior on top.

```python
class Keypad(Widget):
    @elements
    def buttons(self):
        return {
            "web": By.tag_name("button"),
            "mobile": {"Android": By.class_name("<android button class>")},
            "desktop": {"Darwin": By.xpath("<mac button xpath>")},
        }

    def press(self, key: str) -> None:
        index = self._key_to_index(key)
        self.buttons[index].click()
```

Consumers of the widget never deal with indexes or locators — only intent.

---

## Pattern: isolate variability inside the widget

Different platforms often implement “the same component” differently.

Widgets are the correct place to absorb that variability.

- platform-specific locators
- OS-specific attributes
- responsive layout differences

Page Objects and tests stay clean because they only see **resolved elements**, not locator choices.

For detailed rules, refer to:

- `/docs/reference/behavior-contracts/locator-resolution.md`
- `/docs/how-to/os-specific-locators.md`
- `/docs/how-to/platform-agnostic-locators.md`

---

## Pattern: avoid sleeps; wait for observable outcomes

Widgets often trigger asynchronous UI behavior:

- loading indicators
- transitions
- dynamic content updates

Avoid `time.sleep(...)`.

Instead, widget methods should wait for **observable conditions**:
- text appears
- element becomes enabled
- list length increases
- state visibly changes

This keeps widgets stable across devices, environments, and CI conditions.

---

## Pattern: widget reuse inside Page Objects

Page Objects should treat widgets as building blocks.

```python
class Calculator:
    @widget(klass=Keypad)
    def keypad(self):
        pass

    def evaluate_expression(self, a: float, op: str, b: float) -> None:
        self.keypad.evaluate_expression(a, op, b)
```

This keeps Page Objects focused on **screen-level orchestration**, not component internals.

---

## Verify vs assertion in widget-heavy flows

Widgets may contain `verify(...)` calls to explain decisions in logs.

However:

- widgets do not make test assertions
- tests must still end with explicit assertions

This preserves a clear boundary between **diagnostics** and **test outcomes**.


---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Reusable Widget Patterns](/docs/examples/patterns/reusable-widgets.md)  
→ Next: [High-Level Architecture Overview](/docs/architecture/overview.md)
