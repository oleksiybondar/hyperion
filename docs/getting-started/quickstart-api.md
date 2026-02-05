← [Back to Documentation Index](/docs/index.md)  
← Previous: [Quickstart: Web UI Testing](/docs/getting-started/quickstart-web.md)  
→ Next: [Quickstart: CLI Testing](/docs/getting-started/quickstart-cli.md)

---

# 1.5 Quickstart: API Testing

This Quickstart shows a minimal, end-to-end **REST API test** using Hyperion’s `RESTClient`.

The goal is to demonstrate:
- making a request with a reusable client
- asserting success using **`expect`** / **`verify`**
- validating the response using **JSON Schema** in one line

> JSON Schema is especially useful for REST because responses tend to have stable shapes. (GraphQL can still be tested via HTTP, but its response shape is often more query-dependent.)

---

## Minimal setup

This example assumes you already completed:

- [1.1 Installation](/docs/getting-started/installation.md)
- [1.2 Project Setup (pytest)](/docs/getting-started/project-setup-pytest.md)
- [1.3 Basic Configuration](/docs/getting-started/configuration.md)

No extra setup is required beyond pytest.

---

## API client

Hyperion’s `RESTClient` holds the base URL and lets you build simple calls off it.

Even though this example uses a public demo API, treat it as a stand-in for your own service.

```python
from hyperiontf import RESTClient


class PostsAPI:
    """
    Minimal reusable API client for a service exposing `/posts/{id}`.
    """

    def __init__(self):
        self._client = RESTClient("https://jsonplaceholder.typicode.com")

    def get_post(self, post_id: int):
        # GET /posts/{id}
        return self._client.get(path=f"posts/{post_id}")
```

---

## The test

This single test makes one request and validates:
- the response matches a minimal expected JSON shape
- and (optionally) a small semantic check using `verify`

The schema below is intentionally lightweight: it checks types and required fields,
without locking values to a specific snapshot.

```python
import pytest
from hyperiontf import expect, verify
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401
from hyperiontf.executors.pytest import fixture

# If you want to assert schema failures without raising, pass is_assertion=False.
# The method returns a boolean in that mode (as shown in framework tests).


@fixture(scope="function")
def posts_api():
    return PostsAPI()


def test_get_post_schema(posts_api):
    schema = {
        "type": "object",
        "properties": {
            "userId": {"type": "integer"},
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "body": {"type": "string"},
        },
        "required": ["userId", "id", "title", "body"],
    }

    response = posts_api.get_post(1)

    # Critical: schema must match (using non-raising mode so we can show `expect`)
    ok = response.validate_json_schema(schema, is_assertion=False)
    expect(ok).to_equal(True)

    # Non-fatal example: a small extra check (kept intentionally lightweight)
    # Depending on your Response API, this may be a dict already or available via a property.
    # We keep this verify minimal to avoid turning this into a response-parsing tutorial.
    if hasattr(response, "body") and isinstance(response.body, dict):
        verify(response.body.get("id")).to_equal(1)
```

---

## What just happened

- You created a small reusable API client (`PostsAPI`) rather than issuing raw calls inside the test.
- You executed a request with `RESTClient` and validated the response shape using JSON Schema.
- You used **`expect`** for the critical “must pass” check, and **`verify`** for an additional non-fatal check.

---

## What this already demonstrates

- Hyperion REST client usage (`RESTClient`)
- End-to-end request → response → assertion flow
- JSON Schema validation via `response.validate_json_schema(...)`
- Assertion intent (`expect` vs `verify`)

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Quickstart: Web UI Testing](/docs/getting-started/quickstart-web.md)  
→ Next: [Quickstart: CLI Testing](/docs/getting-started/quickstart-cli.md)
