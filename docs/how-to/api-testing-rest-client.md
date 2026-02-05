← [Back to Documentation Index](/docs/index.md)  
← Previous: [Working with WebViews](/docs/how-to/work-with-webviews.md)  
→ Next: [CLI Testing](/docs/how-to/cli-testing-cli-client.md)

---

# How-To: REST / HTTP testing with Hyperion

Hyperion’s REST API is intentionally small: **Client → Request → Response**.
It’s meant to be used in two complementary ways:

1. **API testing** (validate status, headers, schemas, payloads, error responses)
2. **Data preparation** (create/update/delete backend entities with maximum debuggability)

The key advantage of using Hyperion’s client (even for “just setup”) is **one unified execution + logging flow**:
- requests are logged (including a cURL representation)
- responses and failures are logged consistently
- `verify_*` provides **decision logging** without turning setup code into “soft assertions”

---

## Use case A: API testing (assert correctness)

In API tests, prefer:
- `expect(...)` for assertion-style checks (raises on failure)
- explicit test assertions at the end (status codes, required fields, etc.)

### Minimal test: GET health endpoint

```python
from hyperiontf.clients.http import Client
from hyperiontf import expect

def test_health_endpoint():
    client = Client(url="https://api.example.test", accept_errors=False)

    response = client.get(path="/health")

    # Assertions (raise on failure)
    expect(response.status).to_be(200)
    expect(response.headers).to_contain("Content-Type")

    # Explicit test assertion at the end (always)
    assert response.status == 200
```

---

## Use case B: Data preparation (don’t assert inside “models”)

It’s common to prepare test data via backend-only APIs (REST/GraphQL) using small “model” helpers
that provide CRUD operations.

The rule of thumb:
- **Models should not assert** (they are utilities, shared by many tests).
- Models may use `verify(...)` to log decisions and unexpected states while continuing where safe.
- The **test** remains responsible for final assertions.

### Example: a simple CRUD helper (model-style)

This is an intentionally small pattern:
- it returns raw `Response` objects (or extracted IDs)
- it logs via `verify(...)`
- it never asserts correctness on behalf of the test

```python
from hyperiontf.clients.http import Client
from hyperiontf import verify

class UserApi:
    def __init__(self, client: Client):
        self._client = client

    def create_user(self, email: str) -> str:
        # accept_errors=True so setup code can inspect failures without raising immediately
        response = self._client.post(
            path="/users",
            payload={"email": email},
            accept_errors=True,
        )

        # Decision logging (no raising)
        verify(response.status).to_be(201)

        # Keep control flow explicit: return something useful or raise a domain error
        # (If you want this to never raise, return response instead and let the test decide.)
        if response.status != 201:
            raise RuntimeError(f"Failed to create user: status={response.status}")

        user_id = response.body["id"]
        return user_id

    def delete_user(self, user_id: str) -> None:
        response = self._client.delete(path=f"/users/{user_id}", accept_errors=True)
        verify(response.status).to_be(204)
```

### Using the model in a test

The test asserts the outcome it cares about.

```python
from hyperiontf.clients.http import Client
from hyperiontf import expect

def test_user_flow():
    client = Client(url="https://api.example.test")
    users = UserApi(client)

    user_id = users.create_user(email="someone@example.test")

    response = client.get(path=f"/users/{user_id}", accept_errors=False)

    expect(response.status).to_be(200)
    expect(response.body["id"]).to_be(user_id)

    # Explicit test assertion at the end
    assert response.status == 200
```

---

## Validation patterns

### Validate JSON schema (assert vs verify)

`Response.validate_json_schema(schema, is_assertion=...)` integrates with Hyperion expectations.

- Use `is_assertion=True` in tests.
- Use `is_assertion=False` in setup/helpers when you want decision logging.

```python
def test_contract_schema(client: Client, user_schema: dict):
    response = client.get(path="/users/123", accept_errors=False)

    # Assertion semantics (raises)
    response.validate_json_schema(user_schema, is_assertion=True)

    assert response.status == 200
```

---

## Redirects and error handling

### Prefer `accept_errors=False` in tests

In test code, failing fast is usually best:
- `accept_errors=False` makes non-2xx responses raise (contract-level failure)
- you avoid silently continuing on unexpected responses

Use `accept_errors=True` only when the test explicitly validates error payloads.

```python
def test_validation_error_payload(client: Client):
    response = client.post(
        path="/users",
        payload={"email": "not-an-email"},
        accept_errors=True,
    )

    # You are explicitly testing the error response
    assert response.status == 400
```

---

## Polling / waiting for eventual consistency

Some APIs are eventually consistent (create → read may lag).
Hyperion’s core principle is **interactive waiting** (observable checks), not passive `sleep`.

Before documenting the recommended polling primitive here, we need to confirm:
- whether Hyperion provides a **generic wait/poll helper** for REST/API workflows, or
- whether you want the docs to standardize on a small local polling loop pattern.

✅ If you tell me which one is the intended public pattern, I’ll add the polling section with
a concrete, copy-pasteable example (no invented helpers).

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Working with WebViews](/docs/how-to/work-with-webviews.md)  
→ Next: [CLI Testing](/docs/how-to/cli-testing-cli-client.md)
