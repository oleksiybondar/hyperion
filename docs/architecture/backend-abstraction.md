← [Back to Documentation Index](/docs/index.md)  
← Previous: [Locator Resolution Internals](/docs/architecture/locator-resolution.md)

---

# 8.8 Backend Abstraction Layer

Hyperion is designed to support multiple execution domains under a **single, consistent architectural model**.

UI automation, REST APIs, CLI/SSH execution, and visual testing all differ radically in mechanics, but they share common architectural requirements:
- deterministic execution
- stable state management
- consistent logging
- clear separation of intent and execution

The backend abstraction layer is responsible for unifying these domains without leaking backend-specific details into user code.

---

## Backends as execution providers

In Hyperion, a backend is an **execution provider**, not an architectural driver.

Backends are responsible for:
- executing resolved actions
- returning raw results
- reporting backend-level errors

They are *not* responsible for:
- Page Object structure
- locator resolution
- context switching logic
- retries or recovery
- test semantics

All of those concerns live above the backend layer.

---

## UI automation backends

Hyperion currently supports multiple UI automation backends, including:

- Selenium
- Appium
- Playwright
- Windows Application Driver (direct JSONWire usage)

These backends differ in protocol, capabilities, and execution models, but Hyperion treats them uniformly through an **adapter + wrapper** architecture.

### Adapter layer

Adapters:
- normalize backend APIs
- translate backend-specific commands into a common internal interface
- do not invent or reinterpret capabilities

Capabilities are passed through directly.
Hyperion does not define its own capability model.

---

### Wrapper layer

Wrappers:
- extend backend behavior with framework-level features
- integrate retries, waits, and recovery
- participate in context management
- provide consistent error semantics

Wrappers operate on backend objects by reference.
Backend handles may be replaced transparently during recovery.

---

## REST backend architecture

The REST backend follows an **aggregate + override** model.

### REST client

The client:
- holds base configuration (base URL, headers, authentication, cookies, timeouts)
- manages persistent state such as cookies and default headers
- serves as a parent for requests

---

### Request objects

Requests:
- are wrappers around request primitives
- inherit unspecified configuration from the client
- may override any client-level field
- form a parent–child relationship with the client

This allows configuration to be layered without duplication.

---

### Response objects

Responses:
- wrap backend responses
- retain a reference to the originating request
- support schema validation and structured inspection
- participate in logging and diagnostics

This bidirectional linkage enables traceable, debuggable API interactions.

---

## CLI and SSH backends

The CLI backend provides a persistent command execution environment.

Characteristics:
- commands execute within a long-lived session
- output is captured and processed consistently
- exit codes and prompts are observable

---

### SSH as a polymorphic extension

The SSH backend:
- extends the CLI model
- uses Paramiko as the transport
- shares the same interface as CLI
- differs only in command dispatch and output processing

From the framework’s perspective, CLI and SSH are **polymorphic backends** implementing the same execution contract.

---

## Visual testing backend

Visual testing is implemented as a dedicated backend using OpenCV.

### Comparison modes

Hyperion supports two visual comparison modes:

#### Exact (1:1) comparison
- no scaling or normalization is applied
- images must match pixel-for-pixel
- resolution differences are treated as meaningful changes

#### Threshold-based comparison
- bounded visual differences are allowed
- automatic normalization is applied when dimensions differ
- if direct scaling would distort one image, Hyperion computes the closest common dimensions
- both images are scaled to that target before comparison

This distinction is intentional and preserves strict identity checks while enabling tolerant equivalence checks.

---

### Filters and preprocessing

Image filters and preprocessing steps exist to improve practical usability.
They are considered **tuning mechanisms**, not part of the architectural contract.

The normalization and comparison strategy is the architectural guarantee.

---

## Test executors and pytest integration

Hyperion is designed to work with test executors rather than owning test execution itself.

### Pytest integration

Pytest is the primary supported executor.

Hyperion integrates by:
- decorating pytest fixtures and test cases
- detecting test lifecycle boundaries
- establishing consistent logging scopes
- producing structured HTML logs per test case

Pytest is treated as an execution harness, not as a dependency of the core framework.

---

### Other executors

Other executors (e.g. Robot Framework) are conceptually possible.

However, without executor-specific integration:
- test lifecycle detection is limited
- logging and reporting lose fidelity

As of now, pytest provides the richest and most complete execution harness.

---

## Backend neutrality as a core principle

Across all backends, Hyperion enforces the same architectural rule:

> Backends execute. The framework decides *when*, *where*, and *why*.

This neutrality ensures that:
- Page Objects remain backend-agnostic
- test logic remains portable
- new backends can be introduced without rewriting tests

---

## Summary

The backend abstraction layer in Hyperion:

- unifies diverse execution technologies
- isolates backend differences behind adapters
- preserves a single structural and execution model
- supports UI, API, CLI, SSH, and Visual testing
- integrates cleanly with external test executors

With this layer in place, Hyperion can scale horizontally across technologies while preserving a single, coherent architectural identity.

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Locator Resolution Internals](/docs/architecture/locator-resolution.md)  
