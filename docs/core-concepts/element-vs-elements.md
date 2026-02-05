← [Back to Documentation Index](/docs/index.md)  
← Previous: [Pages, Widgets, and Nested Structures](/docs/core-concepts/pages-and-widgets.md)  
→ Next: [Locator Resolution Model](/docs/core-concepts/locator-resolution.md)

---

# Element vs Elements (singular vs plural)

Hyperion makes a deliberate distinction between **Element** and **Elements**.

This distinction is **not** about singular vs plural values, and it is **not** equivalent to
“an element versus an array of elements”.

Instead, it represents two different **modeling contracts** with different expectations,
capabilities, and behavior.

Understanding this difference early is essential for writing stable and expressive tests.

---

## What an Element represents

An **Element** represents a **single, logical UI target**.

When something is modeled as an Element, it carries an implicit contract:

> “There is exactly one meaningful thing here.”

This contract is intentional.

An Element is used when:
- the UI guarantees uniqueness
- multiple matches would indicate a bug or broken state
- the test logic depends on interacting with *the* thing, not *one of many*

Conceptually, an Element represents:
- a button
- an input field
- a title
- a specific control with a single purpose

If the underlying UI changes in a way that violates this expectation, failure is desirable —
it signals that the model no longer matches reality.

---

## What an Elements collection represents

**Elements** represents a **dynamic set of UI targets**, treated as a single conceptual unit.

Unlike Element, an Elements collection:
- does not assume uniqueness
- does not assume a fixed size
- is expected to change over time

Typical examples include:
- lists
- tables
- grids
- menus
- repeated cards or rows

An Elements collection represents:
> “All things that match this structure *right now*.”

This makes Elements suitable for UIs where:
- items are added or removed dynamically
- order may change
- the presence or absence of items is meaningful

---

## Elements is not an array

A critical point in Hyperion’s design is that **Elements is not a simple container type**.

It is **not**:
- a raw list of Element objects
- a passive snapshot of the DOM
- a convenience wrapper around indexing

Instead, Elements is a **first-class abstraction** with its own responsibilities.

Conceptually, an Elements collection:
- represents a *live view* of a set of UI targets
- manages a group of element handles internally
- provides collection-level behavior
- encodes expectations about variability and change

This is why treating Elements as “just an array” leads to fragile models and unstable tests.

The distinction exists to express **intent**, not just quantity.

---

## Why the distinction matters

Choosing between Element and Elements affects more than syntax.

It influences:
- how failures are interpreted
- how waiting and synchronization behave
- how retries and recovery are applied
- how readable and intention-revealing the model is

Modeling something as an Element communicates:
> “If this isn’t exactly one thing, something is wrong.”

Modeling something as Elements communicates:
> “This is a set, and change is expected.”

This allows Hyperion to apply different behavioral strategies internally, while keeping test
code clean and declarative.

In other words:
- Element optimizes for **precision**
- Elements optimizes for **variability**

---

## Choosing between Element and Elements

When deciding how to model something, the following heuristics usually help.

Model something as an **Element** if:
- there should logically be only one
- multiple matches indicate an invalid UI state
- the test depends on interacting with a specific control

Model something as **Elements** if:
- the UI repeats a structure
- the number of items can change
- order or presence is meaningful
- you expect to iterate, filter, or select among items

A simple question often clarifies the choice:

> “Would multiple matches be a bug — or a normal situation?”

If it would be a bug, use Element.  
If it would be normal, use Elements.

---

## Common mistakes and anti-patterns

Certain patterns frequently lead to unstable or misleading models.

### Modeling lists as a single Element
Treating a repeated structure as a single element and relying on “the first match”
hides multiplicity and creates brittle assumptions.

If the UI repeats something, the model should reflect that explicitly.

---

### Treating Elements like a static list
Assuming that an Elements collection is fixed in size or order ignores the dynamic nature
of modern UIs.

Collections exist precisely because change is expected.

---

### Hiding multiplicity inside helper methods
Helper methods that internally pick an index from a collection often obscure intent
and make tests harder to reason about.

It is usually better for the model to expose the collection explicitly.

---

### Using Element when Elements communicates intent better
Sometimes a single item exists *now*, but conceptually represents a list with one entry.

In such cases, modeling it as Elements often better reflects future evolution and avoids
rework when the UI grows.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Pages, Widgets, and Nested Structures](/docs/core-concepts/pages-and-widgets.md)  
→ Next: [Locator Resolution Model](/docs/core-concepts/locator-resolution.md)
