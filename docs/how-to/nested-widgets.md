# 4.7 Nested Widgets

← [/docs/tutorials/widgets-101.md](/docs/tutorials/widgets-101.md)

---

Nested widgets are where Hyperion’s Page Object Model starts to feel truly natural.

If you come from modern frontend development, this should feel familiar:
- pages composed from components
- components composed from smaller components
- each level owning its own behavior

This guide explains **when and how to introduce nested widgets** —
and just as importantly, **when not to**.

---

## When nested widgets make sense

A good rule of thumb:

> If a part of the UI has **its own structure and behavior**,  
> and appears more than once (or could), it wants to be a widget.

Nested widgets are appropriate when:
- a component has internal state or actions
- the same structure appears repeatedly
- test logic naturally groups around that structure
- you want logs to reflect UI hierarchy

They are *not* about abstraction for its own sake.

---

## The Scenario

We’ll model a common real-world UI:

**Dashboard page**
- contains a data table
- each row represents an entity
- each row has an **action menu (dropdown)**

Visually:

```
Dashboard
 └── Table
      └── Row
           └── Action Menu
```

Each level:
- has its own responsibility
- can be reasoned about independently
- maps directly to how the UI is built

---

## Step 1: Start with the smallest meaningful component

We begin at the **action menu** level.

This is a dropdown with behavior:
- open
- click an action

That’s already enough to justify a widget.

```python
from hyperiontf import Widget, element, By


class ActionMenu(Widget):

    @element
    def toggle(self):
        return By.css(".action-menu-toggle")

    @element
    def delete_action(self):
        return By.css(".action-delete")

    def delete(self) -> None:
        self.toggle.click()
        self.delete_action.click()
```

### Why this is a widget

- it has internal state (open / closed)
- it has behavior (`delete`)
- tests should not orchestrate its mechanics

---

## Step 2: Model a table row as a widget

A table row:
- groups multiple columns
- owns the action menu
- represents a single logical entity

That makes it a perfect widget.

```python
from hyperiontf import Widget, element, widget, By
from .action_menu import ActionMenu


class TableRow(Widget):

    @element
    def name(self):
        return By.css(".cell-name")

    @element
    def status(self):
        return By.css(".cell-status")

    @widget(klass=ActionMenu)
    def actions(self):
        return By.css(".cell-actions")

    def delete(self) -> None:
        self.actions.delete()
```

### Design note

Notice how:
- the row exposes **intent-level behavior**
- it does *not* leak menu mechanics
- calling code doesn’t need to know a dropdown exists

---

## Step 3: Model the table itself

The table:
- is a container of rows
- does not need to know row internals
- provides access to rows as a collection

```python
from hyperiontf import Widget, widgets, By
from .table_row import TableRow


class DataTable(Widget):

    @widgets(klass=TableRow)
    def rows(self):
        return By.css("tbody tr")
```

At this point, hierarchy starts paying off:
- each row is a full-featured object
- each row owns its own behavior
- the table remains simple

---

## Step 4: Attach the table to the page

Now we bring everything together on the page.

```python
from hyperiontf import WebPage, widget, element, By
from .data_table import DataTable


class DashboardPage(WebPage):

    @widget(klass=DataTable)
    def users_table(self):
        return By.id("users-table")

    @element
    def success_message(self):
        return By.id("notification")
```

---

## Step 5: Use the hierarchy in a test

Now look at the test code.

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401


def test_delete_user_from_dashboard(dashboard_page):
    dashboard_page.users_table.rows[0].delete()

    dashboard_page.success_message.assert_text(
        "User deleted successfully"
    )
```

This line:

```python
dashboard_page.users_table.rows[0].delete()
```

reads like the UI:
- dashboard
- table
- row
- action

That’s not accidental — that’s the design goal.

---

## How deep is too deep?

Nested widgets are powerful, but depth must be justified.

Ask yourself at each level:
- does this part have its own behavior?
- would tests benefit from naming it?
- does it improve readability or reuse?

If the answer is “no”, keep it flat.

> Hierarchy is a tool — not a goal.

---

## Why this works in Hyperion

Traditional frameworks struggle with deep hierarchies because:
- re-rendering breaks references
- stale elements cascade
- context becomes fragile

Hyperion guarantees:
- automatic stale recovery
- correct facade reassembly
- stable object graphs
- readable, hierarchical logs

This makes nested widgets **safe**, not risky.

---

## Design guidelines

**Good signs you need a nested widget**
- repeated DOM structure
- repeated interaction logic
- mental grouping while reading tests

**Bad signs**
- widget with no behavior
- one-off abstraction
- hierarchy added “just in case”

---

## What You Learned

You now know how to:
- decide when to introduce nested widgets
- model complex UI structures cleanly
- keep behavior close to structure
- avoid over-engineering

Most importantly:

> Nested widgets are not about abstraction.  
> They are about **expressing UI intent clearly and safely**.

---

## Next Guides

From here, you may want to continue with:
- [/docs/how-to/work-with-iframes.md](/docs/how-to/work-with-iframes.md)
- [/docs/how-to/work-with-webviews.md](/docs/how-to/work-with-webviews.md)

Or explore:
- [/docs/how-to/eql-recipes.md](/docs/how-to/eql-recipes.md)

---
← [/docs/tutorials/widgets-101.md](/docs/tutorials/widgets-101.md)