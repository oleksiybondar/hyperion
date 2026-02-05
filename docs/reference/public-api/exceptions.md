← [Back to Documentation Index](/docs/index.md)  
← Previous: [Configuration](/docs/reference/public-api/configuration.md)  
→ Next: [Logger](/docs/reference/public-api/logger.md)

---

# 5.19 Exceptions

This page documents the **public exception hierarchy** used by the Hyperion Testing Framework.

Hyperion exceptions are part of the **public behavioral contract**:
they describe *why* an operation failed and *what category of failure* occurred.
They are **not meant to be caught to stabilize tests**.

In general:

- exceptions indicate **real failures**
- retries and recovery are handled internally by the framework
- tests should fail fast when these exceptions surface

---

## Base exception

### `HyperionException`

All Hyperion-specific exceptions inherit from `HyperionException`.

Purpose:

- serves as a common base type
- captures and caches the last exception execution context
- allows framework-wide classification of failures

Contract guarantees:

- every Hyperion-raised error is an instance of `HyperionException`
- the last raised Hyperion exception is cached for diagnostic purposes

You should **not** rely on the cached execution data for control flow.
It exists solely for diagnostics and logging.

---

## Assertion and timeout exceptions

### `FailedExpectationException`

Raised when an `expect(...)` assertion fails.

Semantics:

- represents a **test assertion failure**
- causes the test to fail immediately
- includes detailed comparison information in logs

This exception is the expected failure mode for incorrect test outcomes.

---

### `TimeoutException`

Raised when a framework operation exceeds its configured timeout.

Typical causes:

- element never becomes available
- UI never reaches a stable state
- operation remains blocked beyond recovery limits

A `TimeoutException` indicates a **real synchronization failure**, not flakiness.

---

## UI-related exceptions

UI exceptions indicate failures related to UI automation, element resolution,
or context/content management.

All UI exceptions inherit from:

### `HyperionUIException`

This category represents **UI-layer failures** across web, mobile, desktop,
and hybrid contexts.

---

### `UnsupportedAutomationTypeException`

Raised when an unsupported automation backend or automation type is requested.

This usually indicates a **configuration or environment error**.

---

### `StaleElementReferenceException`

Raised when an element reference becomes stale and cannot be recovered.

Important:

- Hyperion retries and recovers stale elements automatically
- this exception surfaces **only after recovery is exhausted**

Do not catch this exception in tests.

---

### `NoSuchElementException`

Raised when an element cannot be found within the allowed resolution and timeout bounds.

This indicates:

- incorrect locator declaration, or
- incorrect assumption about UI state

---

### `IncorrectLocatorException`

Raised when a locator declaration is invalid or malformed.

This is a **configuration or Page Object definition error**, not a runtime flake.

---

### `UnsupportedLocatorException`

Raised when a locator type is not supported by the active automation backend.

---

### `ContentSwitchingException`

Raised when switching between different content types fails
(e.g. native ↔ web content).

---

### `ContextSwitchingException`

Raised when switching between contexts fails
(e.g. default document ↔ iframe).

These exceptions indicate **real context resolution failures**.

---

### `UnknownUIException`

Raised when an unexpected UI-related failure occurs that cannot be classified more specifically.

This usually indicates an unrecoverable backend or environment issue.

---

## API (REST/HTTP) exceptions

API exceptions represent failures in REST / HTTP operations.

All API exceptions inherit from:

### `HyperionAPIException`

---

### `FailedHTTPRequestException`

Raised when an HTTP request fails due to an error response
(e.g. non-accepted status codes when `accept_errors` is disabled).

---

### `ExceededRedirectionLimitException`

Raised when the number of HTTP redirects exceeds the configured limit.

---

### `NotARedirectionException`

Raised when a response is treated as a redirection but does not qualify as one.

---

### `ConnectionErrorException`

Raised when a network or connection-level error occurs.

---

### `JSONSchemaFailedAssertionException`

Raised when a response body fails JSON schema validation.

This represents a **contract violation** between client and server.

---

## CLI exceptions

CLI exceptions represent failures during command execution and orchestration.

All CLI exceptions inherit from:

### `HyperionCLIException`

---

### `CommandExecutionTimeoutException`

Raised when a command execution exceeds its allowed timeout.

---

### `CommandExecutionException`

Raised for general command execution failures.

---

### `InvalidCommandException`

Raised when an invalid or unsupported command is issued.

---

### `AuthenticationException`

Raised when authentication fails
(e.g. incorrect credentials or sudo password).

---

### `CommandExpectFailureException`

Raised when an expected pattern is not found in command output.

---

## Exceptions that should not be caught

As a rule:

- **do not catch Hyperion exceptions to stabilize tests**
- **do not retry in test code**
- **do not suppress failures**

If an exception from this hierarchy escapes the framework, it indicates:

- a real failure
- a broken assumption
- a configuration or environment problem

The correct fix is almost always in:

- Page Object definitions
- widget readiness logic
- configuration
- application behavior

---

## Related documentation

- Configuration: `/docs/reference/public-api/configuration.md`
- Logger: `/docs/reference/public-api/logger.md`
- Retry and timeout guarantees: `/docs/reference/behavior-contracts/timeouts.md`
- Writing stable tests: `/docs/how-to/write-stable-tests.md`

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Configuration](/docs/reference/public-api/configuration.md)  
→ Next: [Logger](/docs/reference/public-api/logger.md)