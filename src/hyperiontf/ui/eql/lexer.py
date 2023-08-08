import ply.lex as lex
import re
from hyperiontf.ui.color import Color

from hyperiontf.typing import ElementQueryLanguageParseException

reserved_words = {
    "and": "AND",
    "or": "OR",
    "true": "TRUE",
    "false": "FALSE",
    "attribute": "ATTRIBUTE",
    "style": "STYLE",
}

tokens = (
    "WS",
    "EQUAL",
    "NOTEQUAL",
    "APPROX",
    "LT",
    "LE",
    "GT",
    "GE",
    "DOT",
    "COLON",
    "LBRACKET",
    "RBRACKET",
    "STRING",
    "REGEX",
    "NUMBER",
    "TRUE",
    "FALSE",
    "ATTRIBUTE",
    "STYLE",
    "DATE",
    "AND",
    "OR",
    "ITEM_NAME",
    "HEX_COLOR",
    "SHORT_HEX_COLOR",
    "RGB_COLOR",
    "RGBA_COLOR",
)

t_WS = r"\s+"
t_EQUAL = r"=="
t_NOTEQUAL = r"!="
t_APPROX = r"~="
t_LT = r"<"
t_LE = r"<="
t_GT = r">"
t_GE = r">="
t_DOT = r"\."
t_COLON = r":"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"


def t_STRING(t):
    r""" "[^"]*"|\'[^\']*\'"""
    t.value = t.value[1:-1]
    return t


def t_REGEX(t):
    r"""/([^/]*)/"""
    t.value = re.compile(t.value[1:-1])
    return t


def t_NUMBER(t):
    r"""-?(\d+(\.\d*)?|\.\d+)"""
    t.value = float(t.value) if "." in t.value else int(t.value)
    return t


def t_DATE(t):
    r"""date\([^\)]*\)"""
    t.value = t.value[5:-1]
    return t


def t_ITEM_NAME(t):
    r"""[a-zA-Z][a-zA-Z0-9_\-]*[a-zA-Z0-9_]"""
    t.type = reserved_words.get(t.value, "ITEM_NAME")  # Check for reserved words
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_HEX_COLOR(t):
    r"""\\\#([A-Fa-f0-9]{6})\b"""
    t.value = Color.from_string(t.value)
    return t


def t_SHORT_HEX_COLOR(t):
    r"""\\\#([A-Fa-f0-9]{3})\b"""
    t.value = Color.from_string(t.value)
    return t


def t_RGB_COLOR(t):
    r"""rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)"""
    t.value = Color.from_string(t.value)
    return t


def t_RGBA_COLOR(t):
    r"""rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0?\.\d+|1(\.0+)?)\s*\)"""
    t.value = Color.from_string(t.value)
    return t


t_ignore = " \t"


# Error handling rule
def t_error(t):
    raise ElementQueryLanguageParseException(f"Illegal character '{t.value[0]}'")


lexer = lex.lex()


def tokenize(input_string: str):
    lexer.input(input_string)
    result = []
    while True:
        token = lexer.token()
        if not token:
            break
        result.append(token)
    return result
