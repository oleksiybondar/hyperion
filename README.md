# Hyperion Testing Framework

> "One Framework to unite them all, One Framework to streamline interfaces, One Framework to simplify the way and bring harmony in automation."

Hyperion is a Python testing framework designed to unify **web**, **mobile**, **desktop**, **API**, **CLI**, and **visual testing** under a single, consistent programming model.

Its primary goal is to reduce duplication, improve test stability, and enable **cross-platform test reuse** through a powerful and extensible Page Object Model (POM).

---

## Documentation

Hyperion’s full documentation is available online and covers:

- Getting started guides
- Core concepts and design philosophy
- Step-by-step tutorials
- How-to guides and recipes
- Public API reference
- Architecture and behavior contracts

📖 **Read the documentation here:**  
https://github.com/oleksiybondar/hyperion/blob/main/docs/index.md

---

## Why Hyperion?

Modern applications rarely exist on a single platform.  
The same product often ships as a web app, a mobile app, a desktop app, and exposes APIs and command-line tools — all backed by the same backend services.

Hyperion is built around the idea that **tests should reflect this reality**.

Instead of writing separate test frameworks and page objects for each platform, Hyperion allows you to:

- Reuse **the same page object structures** across platforms
- Encapsulate platform-specific behavior without duplicating test logic
- Test UI, APIs, CLI tools, and visuals using a unified approach

---

## High-Level Architecture

At its core, Hyperion provides:

- A **cross-platform Page Object Model (POM)**  
  (`WebPage`, `MobileScreen`, `DesktopWindow`, `Widget`, `IFrame`, `WebView`)
- A **declarative element definition model** based on decorators
- A **powerful locator resolution system** supporting:
  - platform-specific locators
  - OS-specific locators
  - viewport-responsive locators
- **Automatic context switching** for iframes, nested iframes, and webviews
- Built-in **stale element recovery** and retry logic
- A unified **Wait API** focused on interactive readiness rather than raw timing
- First-class support for:
  - REST API testing
  - CLI and SSH-based testing
  - Visual testing with baseline comparison
- A dual assertion model:
  - `expect` (fail-fast)
  - `verify` (accumulate failures)

Hyperion wraps the complexity of underlying automation tools (Selenium, Playwright, Appium, etc.) behind a stable and expressive API, allowing test code to focus on **intent**, not mechanics.

---

## Installation

```bash
pip install hyperiontf
```