[← Wait API](/docs/reference/public-api/waits.md) | [CLI Client →](/docs/reference/public-api/cli-client.md)

# HTTP Client (REST)

This page documents Hyperion’s **REST / HTTP public API** as a single logical chain:

- `Client` builds and executes HTTP calls (convenience wrappers and request factory).
- `Request` represents a single HTTP request (URL resolution, header/cookie/auth merging, execution).
- `Response` represents the result (parsed body, headers/cookies, redirects, schema validation).

> Hyperion’s REST API is designed for **testability and debuggability**:
> requests are logged as cURL, and responses are logged (or raised) based on status and `accept_errors`.

---

## Client

`Client` is the entry point for REST / HTTP calls. It provides:
- **default URL components** and **default request settings**
- convenience methods (`get`, `post`, …) that create a `Request` and immediately execute it
- a `request(...)` factory that returns a `Request` for delayed execution

### Client.__init__

**Signature**

`Client.__init__(url: Optional[str] = None, scheme: Optional[str] = None, netloc: Optional[str] = None, path: Optional[str] = None, params: Optional[str] = None, query: Optional[str] = None, fragment: Optional[str] = None, headers: Optional[dict] = None, cookies: Optional[dict] = None, auth: Optional[dict] = None, follow_redirects: bool = config.rest.follow_redirects, log_redirects: bool = config.rest.log_redirects, post_redirect_get: bool = config.rest.log_redirects, accept_errors: bool = config.rest.accept_errors, redirections_limit: int = config.rest.redirections_limit, connection_timeout: int = config.rest.connection_timeout, request_timeout: int = config.rest.request_timeout, default_event_logging_level: str = "info", logger = logger) -> None`

**Contract**

Creates a REST client with optional **base URL** and **default request configuration**.  
If `url` is provided, it is parsed into URL components; otherwise the provided URL component arguments are used directly.

Default `headers`, `cookies`, and `auth` are stored and later **merged** into each `Request`.

**Arguments**

- `url`: Base URL to parse into components (scheme, netloc, path, params, query, fragment).
- `scheme`, `netloc`, `path`, `params`, `query`, `fragment`: Base URL components used when `url` is not provided.
- `headers`: Default headers applied to requests created by this client.
- `cookies`: Default cookies applied to requests created by this client.
- `auth`: Default authentication dictionary applied to requests created by this client.
- `follow_redirects`: Default redirect behavior for created requests.
- `log_redirects`: If `True` and redirects are followed, Hyperion performs redirect handling in a way that enables redirect logging.
- `post_redirect_get`: Default redirect behavior for POST (kept as a per-request flag and passed into redirect requests).
- `accept_errors`: Default error handling mode. If `False`, non-2xx responses raise during `Response` construction.
- `redirections_limit`: Default max redirect count (also applied to the underlying client session behavior).
- `connection_timeout`: Default connection timeout seconds (used as part of the request timeout tuple).
- `request_timeout`: Default request/read timeout seconds (used as part of the request timeout tuple).
- `default_event_logging_level`: Default log method name for REST events. Must be `"debug"` or `"info"`.
- `logger`: Logger instance used for request/response events.

**Returns**

- `None`

---

### Client.default_event_logging_level

**Signature**

`Client.default_event_logging_level -> str`  
`Client.default_event_logging_level = value: str -> None`

**Contract**

Gets or sets the default logging level used to emit REST events.

Setting the value validates it.

**Arguments (setter)**

- `value`: Must be `"debug"` or `"info"`.

**Raises**

- `ValueError`: If `value` is not `"debug"` or `"info"`.

**Returns**

- Getter: `str`
- Setter: `None`

---

### Client.get

**Signature**

`Client.get(payload: Optional[dict] = None, url: Optional[str] = None, scheme: Optional[str] = None, netloc: Optional[str] = None, path: Optional[str] = None, params: Optional[str] = None, query: Optional[str] = None, fragment: Optional[str] = None, headers: Optional[dict] = None, cookies: Optional[dict] = None, auth: Optional[dict] = None, follow_redirects: Optional[bool] = None, log_redirects: Optional[bool] = None, post_redirect_get: Optional[bool] = None, accept_errors: Optional[bool] = None, redirections_limit: Optional[int] = None, connection_timeout: Optional[int] = None, request_timeout: Optional[int] = None) -> AnyResponse`

**Contract**

Creates a `Request` with method `HTTPMethod.GET` and immediately executes it.

Arguments override the client defaults for this call. Any `None` values fall back to client defaults.

**Returns**

- `AnyResponse`: a `SuccessResponse`, `RedirectResponse`, or `ErrorResponse` instance.

---

### Client.post / Client.put / Client.delete / Client.patch / Client.head / Client.options

**Signature**

Each method has the same signature as `Client.get(...)`, but uses the corresponding HTTP method:
- `Client.post(...) -> AnyResponse`
- `Client.put(...) -> AnyResponse`
- `Client.delete(...) -> AnyResponse`
- `Client.patch(...) -> AnyResponse`
- `Client.head(...) -> AnyResponse`
- `Client.options(...) -> AnyResponse`

**Contract**

Creates a `Request` for the corresponding HTTP method and immediately executes it.

**Returns**

- `AnyResponse`: a `SuccessResponse`, `RedirectResponse`, or `ErrorResponse` instance.

---

### Client.request

**Signature**

`Client.request(method: HTTPMethodType, payload: Optional[dict] = None, parent_request: Optional[AnyRequest] = None, url: Optional[str] = None, scheme: Optional[str] = None, netloc: Optional[str] = None, path: Optional[str] = None, params: Optional[str] = None, query: Optional[str] = None, fragment: Optional[str] = None, headers: Optional[dict] = None, cookies: Optional[dict] = None, auth: Optional[dict] = None, follow_redirects: Optional[bool] = None, log_redirects: Optional[bool] = None, post_redirect_get: Optional[bool] = None, accept_errors: Optional[bool] = None, redirections_limit: Optional[int] = None, connection_timeout: Optional[int] = None, request_timeout: Optional[int] = None) -> Request`

**Contract**

Builds a `Request` object without executing it.

This is the lowest-level factory in the public REST API. It is used internally for redirect-following as well.

**Arguments**

- `method`: One of `HTTPMethodType` literals: `"GET"`, `"POST"`, `"PUT"`, `"DELETE"`, `"HEAD"`, `"OPTIONS"`, `"PATCH"`.
- `parent_request`: Optional parent request reference (used to bind redirect chains).

Other arguments match the convenience method parameters and override client defaults.

**Returns**

- `Request`

---

## Request

`Request` represents a single HTTP request that can be executed.

It resolves the effective URL from either:
- `url` (when provided), or
- the client’s URL components overridden by per-request components.

It also merges `headers`, `cookies`, and `auth` with client defaults:
- if an override dict is provided, it merges with client defaults (override wins)
- if `None`, the client defaults are used

### Request.__init__

**Signature**

`Request.__init__(client: Any, method: HTTPMethodType, payload: Optional[dict] = None, parent_request: Optional[AnyRequest] = None, url: Optional[str] = None, scheme: Optional[str] = None, netloc: Optional[str] = None, path: Optional[str] = None, params: Optional[str] = None, query: Optional[str] = None, fragment: Optional[str] = None, headers: Optional[dict] = None, cookies: Optional[dict] = None, auth: Optional[dict] = None, follow_redirects: Optional[bool] = None, log_redirects: Optional[bool] = None, post_redirect_get: Optional[bool] = None, accept_errors: Optional[bool] = None, redirections_limit: Optional[int] = None, connection_timeout: Optional[int] = None, request_timeout: Optional[int] = None) -> None`

**Contract**

Creates a request bound to a `Client`.

The request computes and stores:
- effective URL components
- merged headers/cookies/auth
- effective behavior flags (using per-request override when provided; otherwise client default)

**Arguments**

- `client`: Owning `Client`.
- `method`: One of `HTTPMethodType`.
- `payload`: Optional payload (see payload handling in `execute()`).
- `parent_request`: Optional parent request (used for redirect chaining).
- `url` or URL component overrides: URL for this request.
- `headers`, `cookies`, `auth`: Per-request overrides merged with client defaults.
- `follow_redirects`, `log_redirects`, `post_redirect_get`, `accept_errors`: Effective behavior flags.
- `redirections_limit`, `connection_timeout`, `request_timeout`: Effective numeric defaults.

**Returns**

- `None`

---

### Request.execute

**Signature**

`Request.execute() -> AnyResponse`

**Contract**

Executes the request and returns a `Response` object appropriate for the HTTP status code.

During execution:
- Hyperion logs a cURL representation of the request.
- `start_time` and `end_time` are captured around the request call.
- If request execution fails at the transport level, a `ConnectionErrorException` is raised.
- A `Response` object is created and may raise depending on `accept_errors`.
- If both `follow_redirects` and `log_redirects` are `True`, Hyperion uses `Response.follow_redirects()` for redirect handling.

**Payload handling**

If `payload` is truthy:
- If `payload` is a `dict` or `list`: it is sent as JSON and `Content-Type` is set to `application/json` if not already present.
- Otherwise: it is sent as form-encoded and `Content-Type` is set to `application/x-www-form-urlencoded` if not already present.
- If file-like objects are present in a specific dict form (`{"file": ..., "file_name": ..., "file_type": ...}`), they are extracted into a multipart file upload representation and then closed after the request.

**Raises**

- `ConnectionErrorException`: If a request-level exception occurs during execution.

**Returns**

- `AnyResponse`: a `SuccessResponse`, `RedirectResponse`, or `ErrorResponse` instance.

---

### Request.full_url

**Signature**

`Request.full_url -> str`

**Contract**

Returns the fully assembled request URL (scheme, netloc, path, params, query, fragment).

**Returns**

- `str`

---

### Request.logger

**Signature**

`Request.logger -> Any`

**Contract**

Returns the logger configured on the owning `Client`.

**Returns**

- Logger instance

---

## Response

A `Response` wraps the result of a request and provides:
- status code and message
- parsed body (`body`) and raw body (`raw_body`)
- headers and cookies
- redirect handling helpers
- JSON schema validation integrated with Hyperion `Expect`

Response types are specialized by status code:
- `SuccessResponse` for 2xx
- `RedirectResponse` for 3xx
- `ErrorResponse` for non-2xx, non-3xx

### Response.create_response

**Signature**

`Response.create_response(request: Any, response: Any) -> AnyResponse`

**Contract**

Factory that selects a response subtype based on the HTTP status code:
- 2xx → `SuccessResponse`
- 3xx → `RedirectResponse`
- otherwise → `ErrorResponse`

**Arguments**

- `request`: A `Request` instance.
- `response`: A raw response object produced by the underlying HTTP execution.

**Returns**

- `AnyResponse`

---

### Response.__init__

**Signature**

`Response.__init__(request: Any, response: Any) -> None`

**Contract**

Constructs the response wrapper and immediately performs error handling:
- if status is not 2xx and `request.accept_errors` is `False`, it raises `FailedHTTPRequestException`
- otherwise, it logs the response event

**Raises**

- `FailedHTTPRequestException`: For non-2xx responses when `accept_errors` is `False`.

**Returns**

- `None`

---

### Response.status

**Signature**

`Response.status -> int`

**Contract**

HTTP status code.

**Returns**

- `int`

---

### Response.message

**Signature**

`Response.message -> str`

**Contract**

HTTP reason phrase / status message.

**Returns**

- `str`

---

### Response.raw_body

**Signature**

`Response.raw_body -> str`

**Contract**

Raw response body as text.

**Returns**

- `str`

---

### Response.body

**Signature**

`Response.body -> Union[str, dict, object]`

**Contract**

Returns a parsed representation of the body when a supported content type is detected; otherwise returns raw text.

Parsing behavior:
- JSON (`application/json`) → parsed object
- XML / HTML content types (as detected by simple content type mapping) → parsed document object
- On parse errors → returns `raw_body`

**Returns**

- `Union[str, dict, object]`

---

### Response.headers

**Signature**

`Response.headers -> dict`

**Contract**

Returns response headers as a dictionary.

**Returns**

- `dict`

---

### Response.cookies

**Signature**

`Response.cookies -> dict`

**Contract**

Returns response cookies as a dictionary.

**Returns**

- `dict`

---

### Response.follow_redirect

**Signature**

`Response.follow_redirect() -> AnyResponse`

**Contract**

Follows a single redirect **only when the current response is a `RedirectResponse`**.

Redirect target is read from the `Location` header.

**Raises**

- `NotARedirectionException`: If called on a non-redirect response.
- `NotARedirectionException`: If the `Location` header is missing.

**Returns**

- `AnyResponse`: the executed response from the redirect target.

---

### Response.follow_redirects

**Signature**

`Response.follow_redirects(max_redirects: int = config.rest.redirections_limit) -> None`

**Contract**

Follows redirects repeatedly until:
- a non-redirect response is obtained, or
- the redirect limit is exceeded.

**Important (current behavior)**  
This method does not return the final response (it returns `None`). It only raises if the redirection limit is exceeded.

**Arguments**

- `max_redirects`: Maximum redirect count to follow.

**Raises**

- `ExceededRedirectionLimitException`: If redirects are still occurring after `max_redirects` steps.

**Returns**

- `None`

---

### Response.validate_json_schema

**Signature**

`Response.validate_json_schema(schema: Any, is_assertion: bool = True) -> ExpectationResult`

**Contract**

Validates `Response.body` against a JSON Schema using Hyperion `Expect`.

- If `is_assertion` is `True`, failures raise (assertion semantics).
- If `is_assertion` is `False`, failures are reported as a verification result (decision logging semantics).

**Arguments**

- `schema`: JSON schema (file path or in-memory schema object supported by Hyperion `Expect`).
- `is_assertion`: Whether this check is an assertion (`True`) or a verification (`False`).

**Returns**

- `ExpectationResult`

---

## Response subtypes

### SuccessResponse

**Signature**

`class SuccessResponse(Response)`

**Contract**

A `Response` representing a 2xx HTTP status. No additional behavior beyond `Response`.

---

### RedirectResponse

**Signature**

`class RedirectResponse(Response)`

**Contract**

A `Response` representing a 3xx HTTP status. Enables redirect helpers such as `follow_redirect()`.

---

### ErrorResponse

**Signature**

`class ErrorResponse(Response)`

**Contract**

A `Response` representing non-2xx, non-3xx HTTP status codes.

Whether construction raises depends on `Request.accept_errors`.

---

## Example

```python
from hyperiontf.clients.http import Client
from hyperiontf.typing import HTTPHeader, ContentType, AuthType, TokenType

client = Client(
    url="https://api.example.test",
    headers={HTTPHeader.ACCEPT: ContentType.JSON},
    follow_redirects=True,
    accept_errors=False,
)

response = client.get(path="/health")
# Tests should end with explicit assertions (see Expect/Verify docs)
assert response.status == 200
```

---

[← Wait API](/docs/reference/public-api/waits.md) | [CLI Client →](/docs/reference/public-api/cli-client.md)