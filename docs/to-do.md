← [Back to Documentation Index](/docs/index.md)

---

# Versioning note

Versions in the `0.x.y` range are **not experimental, unreliable, or unstable**.

They represent:
- a production-quality framework
- with stable public APIs
- that simply **does not yet cover the full original scope** required to call Hyperion a
  fully unified, cross-platform testing platform.

The transition to `1.0.0` marks **scope completeness**, not a sudden change in quality or stability.

---

# To-do and Roadmap

This page tracks planned work for Hyperion in broad version milestones.

Notes:
- Version buckets express **intent and grouping**, not exact dates.
- Items may be split into multiple tickets during implementation.
- Public API details will be documented in the corresponding reference pages once implemented.

---

## Target: v1.0.0

Goal: ship the first stable release where all initially planned core features are implemented and documented.

### Components
- [ ] **Tabs**
- [ ] **Carousel**

### Database (single feature area)
A read-first, safety-oriented database integration.

- [ ] **Provider adapters**
  - [ ] MySQL
  - [ ] PostgreSQL
  - [ ] SQL Server
  - [ ] Other providers (TBD; based on demand)

- [ ] **Client API**
  - [ ] Read-only operations first (query / get / assert)
  - [ ] Deterministic assertions for test verification

- [ ] **Write operations (high-safety mode)**
  - [ ] Writes require **explicit, strict configuration**
  - [ ] Writes are intended for **controlled data preparation**
  - [ ] Heavy configuration is treated as a safety mechanism to reduce accidental data mutation

---

## Recurring work (not in scope of v1.0.0)

These areas will be expanded incrementally via minor releases, as needed.

- [ ] **Expand `expect` API**
  - Growth is continuous (“infinite surface”) and will be added as real use-cases appear.

- [ ] **Expand UI element `expect` / `verify` API**
  - Added via minor releases when new patterns and stability requirements emerge.

---

## Target: v1.x.y (automation backends)

Focus: improve platform coverage by adding missing automation backends.

### Unix first
- [ ] Add **XDo** automation backend support
- [ ] Add **SikuliX (Python)** automation backend support

### Windows next
- [ ] Add **AutoIt** automation backend support

Notes:
- Windows is reasonably covered by WinAppDriver directly or via Appium.
- Linux/Unix is currently lacking strong desktop automation coverage (CLI-only is insufficient for many teams).

---

## Target: vX.Y.0 (advanced scrolling and partial rendering)

Focus: solve known complex UI problems from legacy projects.

- [ ] **Deterministic scrolling API**
  - Explicit swipers / gestures (mouse down → move → up, touch equivalents)
  - Deterministic direction and finite behavior (no “magic” scrolling)
  - Support for:
    - partial DOM rendering in mobile applications
    - endless scrolling peculiarities
    - scenarios where built-in `scroll_into_view` is not possible or unreliable
  - Requires richer metadata to remain predictable and debuggable

---

## How to use this page

- Use this roadmap for **prioritization and planning**.
- Treat each checkbox item as a candidate for a dedicated feature ticket.
- Implementation and documentation will be tracked per feature area.

---

← [Back to Documentation Index](/docs/index.md)