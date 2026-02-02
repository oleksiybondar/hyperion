← [Back to Documentation Index](/docs/index.md)  
→ Next: [Pages, Widgets, and Nested Structures](/docs/core-concepts/pages-and-widgets.md)

---

# Hyperion Page Object Model (POM)

The Hyperion Page Object Model (POM) defines **how UI systems are modeled**, not just how elements are located or actions are executed.

It is the conceptual foundation that allows Hyperion to support **web**, **mobile**, **desktop**, **API**, **CLI**, and **visual testing** under a single, consistent programming model.

This chapter explains **what the Hyperion POM is**, **why it exists**, and **how to think in it**.

---

## What is the Hyperion POM?

The Hyperion POM is a **structured, hierarchical representation of a system under test**.

At a high level:

- A system is modeled as a **tree**
- The root represents a **top-level surface** (page, screen, window)
- Internal nodes represent **UI components**
- Leaves represent **interactable elements**

The purpose of the POM is **not** to store locators.  
Its purpose is to express **user-facing structure and behavior** in a way that is:

- readable
- reusable
- stable
- portable across platforms

In Hyperion, tests interact with **intentional objects** (pages, widgets, elements), while the framework handles execution concerns such as synchronization, context switching, retries, and logging.

---

## How it differs from traditional POMs

Traditional Page Object Models often evolve into:

- flat classes full of locators
- large helper methods that mix logic and synchronization
- duplicated structures across pages
- test code that leaks low-level automation details

Hyperion’s POM intentionally takes a different direction.

Key differences:

- **Hierarchy over flatness**  
  UI is modeled as nested structures, not a single class with many fields.

- **Composition over inheritance**  
  Behavior is built by assembling pages and widgets, not by extending deep class hierarchies.

- **Behavior-first modeling**  
  Page objects expose meaningful actions and queries, not just raw element access.

- **Automation concerns are framework responsibilities**  
  Waiting, retries, context switching, and recovery are handled by Hyperion, not by test code.

The result is a POM that scales with application complexity instead of collapsing under it.

---

## Top-Level Building Blocks

The Hyperion POM is built from three primary concepts.

### Page Objects

Page objects represent **top-level application surfaces**, such as:

- a web page
- a mobile screen
- a desktop window

A page object typically:

- defines the scope of interaction
- exposes high-level user actions (flows)
- acts as the entry point to nested components

Pages are the roots of the UI tree.

---

### Widgets

Widgets represent **bounded, reusable UI components** that live inside pages or other widgets.

Examples include:

- navigation bars
- dialogs and modals
- cards, rows, or list items
- complex form sections

Widgets allow the POM to reflect **real UI composition**, enabling reuse and clear boundaries.

Widgets may contain:
- other widgets
- elements
- element collections

---

### Elements

Elements represent the **smallest interactable units** in the UI.

They act as handles for:
- clicking
- typing
- reading state
- waiting for conditions

Hyperion distinguishes between:
- a single element
- a collection of elements  

This distinction is fundamental and is covered in detail in a dedicated chapter.

---

## Composition over inheritance

Hyperion strongly favors **composition** as the primary scaling mechanism for page objects.

This means:

- pages are composed of widgets
- widgets are composed of other widgets and elements
- inheritance is shallow and capability-based

This approach:

- mirrors how UIs are actually built
- avoids fragile base-class hierarchies
- makes reuse explicit and intentional
- keeps responsibilities localized

Instead of asking *“what should this page inherit from?”*, the Hyperion POM encourages asking:

> “What components does this page contain?”

---

## Cross-Platform Design

One of the core goals of Hyperion is **cross-platform test reuse**.

The POM supports this by separating:

- **logical structure** (pages, widgets, elements)
- from **platform-specific details** (locators, contexts, backends)

This allows the same conceptual page object to represent:

- a web UI
- a mobile UI
- a desktop UI  

even when their underlying implementations differ.

From the perspective of the POM:
- the structure stays the same
- only resolution details change at runtime

The mechanics of how locators and platforms are resolved are described in later chapters.

---

## What belongs in a Page Object (and what doesn’t)

A clear boundary around page objects is essential for long-term maintainability.

### What belongs in a Page Object

- high-level user actions (e.g. login, submit, search)
- meaningful UI queries (e.g. error message text, visibility states)
- domain-specific synchronization (waiting for UI states relevant to the page)
- navigation between related pages or states

### What does *not* belong in a Page Object

- test assertions
- test orchestration logic
- data generation
- business rules unrelated to UI behavior
- arbitrary sleeps or timing hacks

A useful rule of thumb:

> Page objects describe **how the user interacts with the system**, not **how the test validates outcomes**.

---

← [Back to Documentation Index](/docs/index.md)  
→ Next: [Pages, Widgets, and Nested Structures](/docs/core-concepts/pages-and-widgets.md)