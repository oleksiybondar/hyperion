# Hyperion Testing Framework

> "One Framework to unite them all, One Framework to streamline interfaces, One Framework to simplify the way and bring harmony in automation."

# Hyperion Testing Framework – Documentation

Welcome to the **Hyperion Testing Framework** documentation.

Hyperion is a Python testing framework designed to unify **web**, **mobile**, **desktop**, **API**, **CLI**, and **visual testing** under a single, consistent programming model.  
Its primary goal is to reduce duplication, improve test stability, and enable **cross-platform test reuse** through a powerful and extensible Page Object Model (POM).

This documentation describes **how Hyperion works**, **how to use it effectively**, and **what guarantees it provides**.

---

## 1. Getting Started

Start here if you are new to Hyperion.

- [1.1 Installation](/docs/getting-started/installation.md)
- [1.2 Project Setup (pytest)](/docs/getting-started/project-setup-pytest.md)
- [1.3 Basic Configuration](/docs/getting-started/configuration.md)

### Quickstarts
Minimal, end-to-end examples for different use cases:

- [1.4 Quickstart: Web UI Testing](/docs/getting-started/quickstart-web.md)
- [1.5 Quickstart: API Testing](/docs/getting-started/quickstart-api.md)
- [1.6 Quickstart: CLI Testing](/docs/getting-started/quickstart-cli.md)
- [1.7 Quickstart: Visual Testing](/docs/getting-started/quickstart-visual.md)

---

## 2. Core Concepts

These chapters explain **how to think in Hyperion**, not just how to call APIs.

- [2.1 Hyperion Page Object Model (POM)](/docs/core-concepts/pom.md)
- [2.2 Pages, Widgets, and Nested Structures](/docs/core-concepts/pages-and-widgets.md)
- [2.3 Element vs Elements (singular vs plural)](/docs/core-concepts/element-vs-elements.md)
- [2.4 Locator Resolution Model](/docs/core-concepts/locator-resolution.md)
- [2.5 Automatic Context Switching](/docs/core-concepts/context-switching.md)
- [2.6 Stale Element Recovery and Retries](/docs/core-concepts/retry-and-recovery.md)

---

## 3. Tutorials

Step-by-step guides that introduce Hyperion features progressively.

- [3.1 Your First Web Test](/docs/tutorials/first-web-test.md)
- [3.2 Page Objects 101](/docs/tutorials/page-objects-101.md)
- [3.3 Widgets and Reusable Components](/docs/tutorials/widgets-101.md)
- [3.4 Working with iFrames](/docs/tutorials/iframes-and-context.md)
- [3.5 Expect vs Verify](/docs/tutorials/expect-vs-verify.md)

---

## 4. How-To Guides

Task-oriented guides for real-world problems.

### Stability and Synchronization
- [4.1 Writing Stable Tests](/docs/how-to/write-stable-tests.md)
- [4.2 Wait API and Timeouts](/docs/how-to/handle-waits-and-timeouts.md)
- [4.3 Handling Animations and Dynamic Content](/docs/how-to/handle-animations.md)

### Locators
- [4.4 Responsive (Viewport-Specific) Locators](/docs/how-to/responsive-locators.md)
- [4.5 OS-Specific Locators](/docs/how-to/os-specific-locators.md)
- [4.6 Platform-Agnostic Locators](/docs/how-to/platform-agnostic-locators.md)

### Advanced UI Structures
- [4.7 Nested Widgets](/docs/how-to/nested-widgets.md)
- [4.8 Working with iFrames](/docs/how-to/work-with-iframes.md)
- [4.9 Working with WebViews](/docs/how-to/work-with-webviews.md)

### Other Testing Domains
- [4.10 REST API Testing](/docs/how-to/api-testing-rest-client.md)
- [4.11 CLI Testing](/docs/how-to/cli-testing-cli-client.md)
- [4.12 SSH Testing](/docs/how-to/ssh-testing-ssh-client.md)
- [4.13 Visual Testing and Baselines](/docs/how-to/visual-testing-baselines.md)

### Querying and Assertions
- [4.14 Elements Query Language (EQL) Recipes](/docs/how-to/eql-recipes.md)
- [4.15 Logging and Reporting](/docs/how-to/logging-and-reports.md)

---

## 5. API Reference

Authoritative reference for Hyperion’s **public API**.

### Page Objects
- [5.1 WebPage](/docs/reference/public-api/webpage.md)
- [5.2 MobileScreen](/docs/reference/public-api/mobilescreen.md)
- [5.3 DesktopWindow](/docs/reference/public-api/desktopwindow.md)
- [5.4 Widget](/docs/reference/public-api/widget.md)
- [5.5 IFrame](/docs/reference/public-api/iframe.md)
- [5.6 WebView](/docs/reference/public-api/webview.md)

### Elements and Actions
- [5.7 Element](/docs/reference/public-api/element.md)
- [5.8 Elements](/docs/reference/public-api/elements.md)
- [5.9 By](/docs/reference/public-api/by.md)
- [5.10 ActionBuilder](/docs/reference/public-api/action-builder.md)

### Assertions and Waiting
- [5.11 Expect](/docs/reference/public-api/expect.md)
- [5.12 Verify](/docs/reference/public-api/verify.md)
- [5.13 Wait API](/docs/reference/public-api/waits.md)

### Clients
- [5.14 REST Client](/docs/reference/public-api/http-client.md)
- [5.15 CLI Client](/docs/reference/public-api/cli-client.md)
- [5.16 SSH Client](/docs/reference/public-api/ssh-client.md)
- [5.17 Visual Testing API](/docs/reference/public-api/visual.md)

### Configuration and Errors
- [5.18 Configuration](/docs/reference/public-api/configuration.md)
- [5.19 Exceptions](/docs/reference/public-api/exceptions.md)
- [5.20 Logger](/docs/reference/public-api/logger.md)

---

## 6. Behavior Contracts

These chapters define **framework guarantees and rules**.

- [6.1 Locator Resolution Order](/docs/reference/behavior-contracts/locator-resolution.md)
- [6.2 Context Switching Rules](/docs/reference/behavior-contracts/context-switching.md)
- [6.3 Retry and Timeout Semantics](/docs/reference/behavior-contracts/timeouts.md)
- [6.4 Logging Behavior](/docs/reference/behavior-contracts/logging.md)

---

## 7. Examples

Curated examples derived from real tests.

- [7.1 Cross-Platform Calculator Example](/docs/examples/patterns/cross-platform-calculator.md)
- [7.2 Reusable Widget Patterns](/docs/examples/patterns/reusable-widgets.md)
- [7.3 Page Object Layout Patterns](/docs/examples/patterns/page-object-layouts.md)


---

## 8. Architecture

These chapters describe how Hyperion is built internally and how it behaves at runtime.

- [8.1 High-Level Architecture Overview](/docs/architecture/overview.md)
- [8.2 Execution Model](/docs/architecture/execution-model.md)
- [8.3 Page Object Lifecycle](/docs/architecture/page-object-lifecycle.md)
- [8.4 Element Resolution and Caching](/docs/architecture/element-resolution.md)
- [8.5 Waits, Retries, and Synchronization](/docs/architecture/waits-and-retries.md)
- [8.6 Context Switching Internals](/docs/architecture/context-switching.md)
- [8.7 Locator Resolution Internals](/docs/architecture/locator-resolution.md)
- [8.8 Backend Abstraction Layer](/docs/architecture/backend-abstraction.md)

---

## License

Hyperion Testing Framework is licensed under the Apache License 2.0.