← [Back to Documentation Index](/docs/index.md)  
← Previous: [Expect](/docs/reference/public-api/expect.md)  
→ Next: [Wait API](/docs/reference/public-api/waits.md)

---

# Verify

`verify(...)` is Hyperion’s **verification-oriented expectation API**.

It uses the **same matcher surface** as `expect(...)` but differs in **failure behavior**.
`verify(...)` is designed for **decision logging**, not for asserting test correctness.

This page documents:
- the `verify(...)` entry point
- behavioral differences vs `expect(...)`
- recommended usage patterns

The matcher API itself is **identical** to `Expect` and is documented in:
- [`Expect` API](/docs/reference/public-api/expect.md)

---

## Entry point

### verify

**Signature**

`verify(actual_value: Any, value_type: Optional[str] = None, content_type: Optional[str] = None, logger: Optional[Logger] = None, sender: str = LoggerSource.EXPECT) -> Expect`

**Contract**

Creates a verification-oriented `Expect` bound to `actual_value`.

- **On success:** returns an `ExpectationResult`
- **On failure:** returns an `ExpectationResult` (does not raise)
- **On type mismatch:** raises immediately

The returned object exposes the **same matcher methods** as `expect(...)`.

**Arguments**

- `actual_value`: The value under verification.
- `value_type`: Optional type hint.
- `content_type`: Optional content hint.
- `logger`: Optional logger override.
- `sender`: Log sender identifier.

**Returns**

- `Expect`

---

## Behavioral differences vs `expect(...)`

| Aspect | expect(...) | verify(...) |
|------|-------------|-------------|
| Failure behavior | Raises immediately | Returns `ExpectationResult` |
| Success behavior | Returns `ExpectationResult` | Returns `ExpectationResult` |
| Type mismatch | Raises immediately | Raises immediately |
| Intended use | Assertions | Decision logging |

> **Important**
>
> `verify(...)` is **not** a soft assertion mechanism.
> It is a logging and control-flow tool.
> Tests must still end with explicit assertions.

---

## ExpectationResult and control flow

All matchers invoked via `verify(...)` return an `ExpectationResult`.

`ExpectationResult` implements boolean conversion.

### ExpectationResult.__bool__

**Signature**

`ExpectationResult.__bool__() -> bool`

**Contract**

- Returns `True` when the verification passed
- Returns `False` when it failed

This enables explicit, readable control flow.

---

## Recommended usage patterns

### Decision logging in setup / helper code

Use `verify(...)` in utilities, models, and setup code where:
- failures should be logged
- control flow should remain explicit
- assertions would be premature

```python
from hyperiontf import verify

def create_user(api, payload):
    response = api.create_user(payload, accept_errors=True)

    if not verify(response.status).to_be(201):
        raise RuntimeError(
            f"User creation failed: status={response.status}"
        )

    return response.body["id"]
```

---

### Combining verify with final assertions

A test may use `verify(...)` for intermediate decisions
but must assert correctness explicitly.

```python
from hyperiontf import verify, expect

def test_flow(response):
    if not verify(response.status).to_be_in_range(200, 299):
        # log unexpected intermediate state
        ...

    expect(response.status).to_be(200)
    assert response.status == 200
```

---

## Matcher API

The matcher API exposed by `verify(...)` is **identical** to `expect(...)`.

See:
- [`Expect` API Reference](/docs/reference/public-api/expect.md)

This includes:
- type-insensitive matchers
- type-specific matchers (string, numeric, collections, mapping, filesystem, image)
- immediate failure on type mismatch

---

## Summary

Use `verify(...)` when you need:
- observability
- debuggability
- explicit control flow

Use `expect(...)` when you need:
- assertions
- contract enforcement
- test correctness guarantees

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Expect](/docs/reference/public-api/expect.md)  
→ Next: [Wait API](/docs/reference/public-api/waits.md)
