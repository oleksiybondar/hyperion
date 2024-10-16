import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401
from hyperiontf import RESTClient


@pytest.mark.REST
@pytest.mark.get
def test_simple_get():
    RESTClient("http://example.com").get()


@pytest.mark.REST
@pytest.mark.get
@pytest.mark.redirect
def test_built_in_redirect():
    # redirect to https
    RESTClient("http://google.com").get()


@pytest.mark.REST
@pytest.mark.get
@pytest.mark.redirect
def test_built_own_redirect():
    # redirect to https
    RESTClient("http://google.com").get(
        follow_redirects=False, accept_errors=True
    ).follow_redirect()


@pytest.mark.REST
@pytest.mark.get
@pytest.mark.JSON_Schema
def test_json_schema_positive():
    schema1 = {
        "type": "object",
        "properties": {
            "userId": {"type": "integer", "const": 1},
            "id": {"type": "integer", "const": 1},
            "title": {
                "type": "string",
                "const": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            },
            "body": {
                "type": "string",
                "const": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit"
                " molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
            },
        },
        "required": ["userId", "id", "title", "body"],
    }

    schema2 = {
        "type": "object",
        "properties": {
            "userId": {"type": "integer"},
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "body": {"type": "string"},
        },
        "required": ["userId", "id", "title", "body"],
    }

    # redirect to https
    response = RESTClient("https://jsonplaceholder.typicode.com").get(path="posts/1")
    response.validate_json_schema(schema1)
    response.validate_json_schema(schema2)


@pytest.mark.REST
@pytest.mark.get
@pytest.mark.JSON_Schema
def test_json_schema_negative():
    schema1 = {
        "type": "object",
        "properties": {
            "userId": {"type": "integer", "const": 1},
            "id": {"type": "integer", "const": 1},
            "title": {"type": "string", "const": "This is a wrong title"},
            "body": {
                "type": "string",
                "const": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
            },
        },
        "required": ["userId", "id", "title", "body"],
    }

    schema2 = {
        "type": "object",
        "properties": {
            "userId": {"type": "integer", "const": 1},
            "id": {"type": "string"},
            "title": {
                "type": "string",
                "const": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            },
        },
        "required": ["userId", "id", "title", "body"],
    }

    # redirect to https
    response = RESTClient("https://jsonplaceholder.typicode.com").get(path="posts/1")
    assert not response.validate_json_schema(schema1, is_assertion=False)
    assert not response.validate_json_schema(schema2, is_assertion=False)
