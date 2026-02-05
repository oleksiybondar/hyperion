← [Back to Documentation Index](/docs/index.md)  
← Previous: [Hyperion Page Object Model (POM)](/docs/core-concepts/pom.md)  
→ Next: [Element vs Elements (singular vs plural)](/docs/core-concepts/element-vs-elements.md)

---

# Pages, Widgets, and Nested Structures

Hyperion models user interfaces as **structured hierarchies**, not flat collections of locators.

Understanding how **pages**, **widgets**, and **nested structures** work together is essential for building page objects that are readable, reusable, and scalable as applications grow.

This chapter explains **how to structure your UI model**, not how to implement locators or interactions.

---

## Pages as roots of interaction

A **page** represents a **top-level surface** that a user can navigate to or interact with as a whole.

Examples include:
- a web page
- a mobile screen
- a desktop window
- a CLI session entry point

Pages act as:
- the **root of a UI tree**
- the **scope boundary** for interactions
- the **entry point** for user flows

A page object typically:
- exposes high-level actions (e.g. “login”, “create user”, “open settings”)
- owns global UI components (headers, navigation, main content areas)
- provides access to nested widgets

Pages should **not** try to model every UI detail directly.  
Instead, they should delegate structure and behavior downward.

---

## Widgets as reusable UI components

A **widget** represents a **bounded UI component** that lives inside a page or another widget.

Widgets exist to model:
- reusable components
- repeated UI structures
- logical boundaries within a page

Examples include:
- navigation bars
- dialogs and modals
- cards, rows, list items
- complex form sections

Widgets are first-class citizens in Hyperion’s POM.  
They are not just namespaces — they encapsulate **structure and behavior**.

A good mental model is:

> If a UI component has its own behavior or internal structure, it probably deserves a widget.

Widgets can:
- contain elements
- contain collections of elements
- contain other widgets

This makes them the primary tool for keeping page objects small and focused.

---

## Nesting and hierarchy

Hyperion encourages **nesting**, because modern UIs are inherently nested.

Conceptually, a UI model often looks like this:

```bash
Page
├─ HeaderWidget
│   ├─ NavigationWidget
│   └─ UserMenuWidget
├─ ContentWidget
│   ├─ FilterPanelWidget
│   └─ ResultsListWidget
│       └─ ResultItemWidget
└─ FooterWidget
```

This hierarchy:
- mirrors how the UI is actually built
- makes relationships explicit
- improves readability over flat access patterns

Deep access paths are not a problem if they are **meaningful**.  
In practice, a path like:

> “page → results → item → action”

is far easier to reason about than a single locator with many conditions.

---

## Widget collections and repeated structures

Many UIs contain **repeated components**:
- lists
- tables
- grids
- card layouts

In Hyperion, these are modeled as **collections of widgets**, not as duplicated logic.

This allows you to:
- represent each item as a coherent unit
- iterate over items naturally
- access individual items by index or condition
- keep behavior close to the component it belongs to

Treat repeated UI elements as a modeling signal:

> If the UI repeats a structure, your POM should repeat a component — not copy code.

This approach keeps page objects stable even as the number of items changes dynamically.

---

## Pages vs Widgets: how to decide

A common question is whether something should be modeled as a **page** or a **widget**.

The following heuristics usually help.

Model something as a **Page** if:
- it represents a navigable surface
- it can be opened or activated independently
- it serves as an entry point for a user flow

Model something as a **Widget** if:
- it is reused across pages
- it has internal behavior or structure
- it logically belongs *inside* a page
- extracting it makes the page API cleaner

If you are unsure, ask:

> “Does this represent *where* the user is, or *what part* of the UI they are interacting with?”

The former points to a page.  
The latter almost always points to a widget.

---

## Common structuring mistakes

Certain patterns tend to cause problems as test suites grow.

### Putting everything in one page object
This leads to:
- oversized classes
- duplicated logic
- unreadable tests

Widgets exist specifically to prevent this.

---

### Using widgets only as namespaces
If a widget contains no behavior and only groups locators, it is often a sign that:
- behavior is leaking into tests
- or the widget boundary is unclear

Widgets should encapsulate **meaningful interactions**, not just structure.

---

### Copying locators instead of modeling components
Copy-paste is often a symptom that:
- a reusable widget is missing
- or the UI structure is not being modeled explicitly

Duplication at the POM level almost always becomes instability later.

---

### Exposing too many low-level elements from pages
If a page exposes dozens of raw elements, tests tend to:
- become tightly coupled to UI details
- bypass intended flows
- break when the UI changes

Prefer exposing **actions and widgets** over raw elements.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Hyperion Page Object Model (POM)](/docs/core-concepts/pom.md)  
→ Next: [Element vs Elements (singular vs plural)](/docs/core-concepts/element-vs-elements.md)