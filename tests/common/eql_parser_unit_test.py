import pytest
import re
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401
from hyperiontf import expect
from hyperiontf.ui.eql.parser import parse

positive = [
    # Simple comparisons
    # 0
    {
        "eql": 'name == "John"',
        "ast": {
            "type": "comparison",
            "left": {"type": "element_chain", "value": [{"name": "name"}]},
            "operator": "==",
            "right": {"type": "string", "value": "John"},
        },
    },
    # 1
    {
        "eql": "age > 18",
        "ast": {
            "type": "comparison",
            "left": {"type": "element_chain", "value": [{"name": "age"}]},
            "operator": ">",
            "right": {"type": "number", "value": 18},
        },
    },
    # 2
    {
        "eql": "amount <= 500.50",
        "ast": {
            "type": "comparison",
            "left": {"type": "element_chain", "value": [{"name": "amount"}]},
            "operator": "<=",
            "right": {"type": "number", "value": 500.50},
        },
    },
    # Complex comparisons
    # 3
    {
        "eql": "10 < age < 50",
        "ast": {
            "type": "logical_expression",
            "operator": "and",
            "left": {
                "type": "comparison",
                "left": {"type": "number", "value": 10},
                "operator": "<",
                "right": {"type": "element_chain", "value": [{"name": "age"}]},
            },
            "right": {
                "type": "comparison",
                "left": {"type": "element_chain", "value": [{"name": "age"}]},
                "operator": "<",
                "right": {"type": "number", "value": 50},
            },
        },
    },
    # Element chain query
    # 4
    {
        "eql": 'user.name == "John"',
        "ast": {
            "type": "comparison",
            "left": {
                "type": "element_chain",
                "value": [{"name": "user"}, {"name": "name"}],
            },
            "operator": "==",
            "right": {"type": "string", "value": "John"},
        },
    },
    # 5
    {
        "eql": 'user.friends[0].name == "Jane"',
        "ast": {
            "type": "comparison",
            "left": {
                "type": "element_chain",
                "value": [
                    {"name": "user"},
                    {"name": "friends", "type": "element"},
                    {"type": "element", "index": 0},
                    {"name": "name"},
                ],
            },
            "operator": "==",
            "right": {"type": "string", "value": "Jane"},
        },
    },
    # Logical operators
    # 6
    {
        "eql": 'name == "John" and age > 30',
        "ast": {
            "type": "logical_expression",
            "left": {
                "type": "comparison",
                "left": {"type": "element_chain", "value": [{"name": "name"}]},
                "operator": "==",
                "right": {"type": "string", "value": "John"},
            },
            "operator": "and",
            "right": {
                "type": "comparison",
                "left": {"type": "element_chain", "value": [{"name": "age"}]},
                "operator": ">",
                "right": {"type": "number", "value": 30},
            },
        },
    },
    # Using different types of values
    # 7
    {
        "eql": "isActive == true",
        "ast": {
            "type": "comparison",
            "left": {"type": "element_chain", "value": [{"name": "isActive"}]},
            "operator": "==",
            "right": {"type": "bool", "value": True},
        },
    },
    # 8
    {
        "eql": "birthDate == date(2023-08-12)",
        "ast": {
            "type": "comparison",
            "left": {"type": "element_chain", "value": [{"name": "birthDate"}]},
            "operator": "==",
            "right": {"type": "date", "value": "2023-08-12"},
        },
    },
    # Segment with attribute type
    # 9
    {
        "eql": 'attribute:metadata == "1.0.0"',
        "ast": {
            "type": "comparison",
            "left": {
                "type": "element_chain",
                "value": [
                    {"name": "metadata", "attr_type": "attribute", "type": "attribute"}
                ],
            },
            "operator": "==",
            "right": {"type": "string", "value": "1.0.0"},
        },
    },
    # Complex chain with mix of elements
    # 10
    {
        "eql": 'person.contacts[1].email == "example@email.com"',
        "ast": {
            "type": "comparison",
            "left": {
                "type": "element_chain",
                "value": [
                    {"name": "person"},
                    {"name": "contacts", "type": "element"},
                    {"type": "element", "index": 1},
                    {"name": "email"},
                ],
            },
            "operator": "==",
            "right": {"type": "string", "value": "example@email.com"},
        },
    },
    # Complex chain with mix of elements and attributes
    # 11
    {
        "eql": 'person.contacts[1].email.style:backgroundColor == "example@email.com"',
        "ast": {
            "type": "comparison",
            "left": {
                "type": "element_chain",
                "value": [
                    {"name": "person"},
                    {"name": "contacts", "type": "element"},
                    {"type": "element", "index": 1},
                    {"name": "email"},
                    {
                        "name": "backgroundColor",
                        "attr_type": "style",
                        "type": "attribute",
                    },
                ],
            },
            "operator": "==",
            "right": {"type": "string", "value": "example@email.com"},
        },
    },
    # Using OR operator
    # 12
    {
        "eql": 'name == "John" or age < 20',
        "ast": {
            "type": "logical_expression",
            "left": {
                "type": "comparison",
                "left": {"type": "element_chain", "value": [{"name": "name"}]},
                "operator": "==",
                "right": {"type": "string", "value": "John"},
            },
            "operator": "or",
            "right": {
                "type": "comparison",
                "left": {"type": "element_chain", "value": [{"name": "age"}]},
                "operator": "<",
                "right": {"type": "number", "value": 20},
            },
        },
    },
    # Using AND operator
    # 13
    {
        "eql": 'name == "John" and age < 30',
        "ast": {
            "type": "logical_expression",
            "left": {
                "type": "comparison",
                "left": {"type": "element_chain", "value": [{"name": "name"}]},
                "operator": "==",
                "right": {"type": "string", "value": "John"},
            },
            "operator": "and",
            "right": {
                "type": "comparison",
                "left": {"type": "element_chain", "value": [{"name": "age"}]},
                "operator": "<",
                "right": {"type": "number", "value": 30},
            },
        },
    },
    # Regex literal
    # 14
    {
        "eql": "pattern ~= /[A-Za-z0-9]+/",
        "ast": {
            "type": "comparison",
            "left": {"type": "element_chain", "value": [{"name": "pattern"}]},
            "operator": "~=",
            "right": {"type": "regex", "value": re.compile("[A-Za-z0-9]+")},
        },
    },
]


@pytest.mark.ElementsQueryLanguage
@pytest.mark.Parse
@pytest.mark.Correct
@pytest.mark.Switching
@pytest.mark.parametrize("sample", positive)
def test_auto_resolve_context_switching_between_multiple_windows(sample):
    """
    Test the EQL parser's ability to correctly parse various EQL expressions into their corresponding ASTs.

    This test iterates over a series of predefined EQL expressions, each accompanied by its expected AST structure. It validates the parser's capability to handle different types of expressions, including simple and complex comparisons, logical expressions, element chain queries, and more, ensuring accurate parsing and AST generation.

    Args:
        sample (dict): A dictionary containing the 'eql' key for the EQL expression and the 'ast' key for the expected AST.
    """
    expect(parse(sample["eql"])).to_be(sample["ast"])
