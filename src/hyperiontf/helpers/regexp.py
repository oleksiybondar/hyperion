from typing import Union
import re

_REGEX_LITERAL = re.compile(r"^/(.*?)/$")  # /pattern/
_REGEX_INLINE_FLAGS = re.compile(r"^\(\?[aiLmsux-]+\)")  # (?i) (?im) (?s) ...


def is_regex(value: Union[str, re.Pattern]) -> bool:
    """
    Determine whether a value should be treated as a regex pattern.

    Supported forms:
      1) compiled regex: re.compile(...)
      2) JS style literal: /pattern/ or /pattern/i
      3) Python inline flags: (?i)pattern

    We intentionally DO NOT guess based on characters like * + ?
    because that causes false positives in normal text.
    """

    # 1) already compiled regex
    if isinstance(value, re.Pattern):
        return True

    if not isinstance(value, str):
        return False

    # 2) /pattern/flags syntax
    if _REGEX_LITERAL.match(value):
        return True

    # 3) inline flags at beginning: (?i)pattern
    if _REGEX_INLINE_FLAGS.match(value):
        return True

    return False


def regexp_to_eql(value: Union[str, re.Pattern]) -> str:
    """
    Convert a regex-ish value into an EQL-style /pattern/ (optionally /pattern/flags).

    Supported inputs:
      - compiled regex: re.Pattern -> uses .pattern
      - already literal: "/pattern/" or "/pattern/i" -> returned as-is
      - plain string: "abc" -> becomes "/abc/"

    Notes:
      - This does not guess intent. If you pass a normal string, we wrap it.
      - We escape '/' in patterns to avoid breaking /.../ format.
    """
    if isinstance(value, re.Pattern):
        pattern = value.pattern
        pattern = pattern.replace("/", r"\/")
        return f"/{pattern}/"

    if not isinstance(value, str):
        raise TypeError(f"Expected str or re.Pattern, got {type(value)!r}")

    # If user already provided /pattern/flags, keep it
    if _REGEX_LITERAL.match(value):
        return value

    return f"/{value}/"
