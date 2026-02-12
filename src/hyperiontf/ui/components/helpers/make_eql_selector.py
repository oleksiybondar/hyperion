import re
from typing import Union

from hyperiontf.helpers.regexp import regexp_to_eql, is_regex


def make_eql_selector(expression: Union[str, re.Pattern], attribute: str = "text"):
    """
    Build an EQL comparison predicate from a string or regular expression.

    The function converts a literal string into an equality comparison and a
    compiled regular expression into a regex match comparison using the EQL
    `~=` operator.

    Examples:
        >>> make_eql_selector("hello")
        'text == "hello"'

        >>> make_eql_selector(re.compile(r"err.*"), "message")
        'message ~= /err.*/'

    Args:
        expression:
            A literal string for exact matching, or a compiled ``re.Pattern``
            for regex matching.
        attribute:
            The EQL field name to compare against. Defaults to ``"text"``.

    Returns:
        str:
            An EQL predicate string suitable for use inside a ``where`` clause.

    Notes:
        The function does not escape field names. Ensure ``attribute`` is a
        valid EQL identifier.
    """
    if is_regex(expression):
        return f"{attribute} ~= {regexp_to_eql(expression)}"
    return f'{attribute} == "{expression}"'
