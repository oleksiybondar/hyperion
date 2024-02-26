import ply.yacc as yacc

from hyperiontf.typing import ElementQueryLanguageParseException, AST
from .lexer import tokens  # noqa: F401


def p_expression(p):
    """expression : comparison_expression expression_tail
    | comparison_expression"""
    if len(p) == 3:
        p[0] = {
            "type": AST.LOGICAL_EXPRESSION,
            "left": p[1],
            "operator": p[2]["operator"],
            "right": p[2]["right"],
        }
    else:
        p[0] = p[1]


def p_expression_tail(p):
    """expression_tail : logical_operator expression"""
    p[0] = {"operator": p[1], "right": p[2]}


def p_simple_comparison(p):
    """simple_comparison : operand comparison_operator operand
    | operand WS comparison_operator WS operand"""
    if len(p) == 4:
        p[0] = {"type": AST.COMPARISON, "left": p[1], "operator": p[2], "right": p[3]}
    else:
        p[0] = {"type": AST.COMPARISON, "left": p[1], "operator": p[3], "right": p[5]}


def p_comparison_expression(p):
    """comparison_expression : simple_comparison comparison_operator operand
    | simple_comparison"""
    length = len(p)
    if length == 2:
        p[0] = p[1]
    else:
        if length == 6:
            right_operator = p[3]
            right = p[5]
        else:
            right_operator = p[2]
            right = p[3]
        p[0] = {
            "type": AST.LOGICAL_EXPRESSION,
            "operator": "and",
            "left": {
                "type": AST.COMPARISON,
                "left": p[1]["left"],
                "operator": p[1]["operator"],
                "right": p[1]["right"],
            },
            "right": {
                "type": AST.COMPARISON,
                "left": p[1]["right"],
                "operator": right_operator,
                "right": right,
            },
        }


def p_operand(p):
    """operand : value
    | element_chain_query"""
    p[0] = p[1]


def p_element_chain_query(p):
    """element_chain_query : element_chain_query DOT segment
    | segment
    """
    if len(p) == 2:
        p[0] = {"type": AST.ELEMENT_CHAIN, "value": [p[1]]}
    else:
        p[0] = p[1]
        if isinstance(p[3], dict):
            p[0]["value"].append(p[3])
        else:
            p[0]["value"] = p[0]["value"] + p[3]


def p_segment(p):
    """segment : identifier
    | identifier COLON attribute_type
    | identifier LBRACKET index RBRACKET"""
    p[0] = {"name": p[1]}
    length = len(p)
    if length == 4:
        p[0]["attr_type"] = p[3]
        p[0]["type"] = AST.ATTRIBUTE
    elif length == 5:
        p[0]["type"] = AST.ELEMENT
        p[0] = [p[0], {"index": p[3], "type": AST.ELEMENT}]


def p_identifier(p):
    """identifier : ITEM_NAME"""
    p[0] = p[1]


def p_attribute_type(p):
    """attribute_type : ATTRIBUTE
    | STYLE"""
    p[0] = p[1]


def p_index(p):
    """index : NUMBER"""
    p[0] = p[1]


def p_comparison_operator(p):
    """comparison_operator : LT
    | LE
    | GT
    | GE
    | EQUAL
    | NOTEQUAL
    | APPROX"""
    p[0] = p[1]


def p_value_string(p):
    """value : STRING"""
    p[0] = {"type": AST.STRING, "value": p[1]}


def p_value_regex(p):
    """value : REGEX"""
    p[0] = {"type": AST.REGEX, "value": p[1]}


def p_value_number(p):
    """value : NUMBER"""
    p[0] = {"type": AST.NUMBER, "value": p[1]}


def p_value_true(p):
    """value : TRUE"""
    p[0] = {"type": AST.BOOL, "value": True}


def p_value_false(p):
    """value : FALSE"""
    p[0] = {"type": AST.BOOL, "value": False}


def p_value_date(p):
    """value : DATE"""
    p[0] = {"type": AST.DATE, "value": p[1]}


def p_value_hex_color(p):
    """value : HEX_COLOR"""
    p[0] = {"type": AST.COLOR, "value": p[1]}


def p_value_short_hex_color(p):
    """value : SHORT_HEX_COLOR"""
    p[0] = {"type": AST.COLOR, "value": p[1]}


def p_value_rgb_color(p):
    """value : RGB_COLOR"""
    p[0] = {"type": AST.COLOR, "value": p[1]}


def p_value_rgba_color(p):
    """value : RGBA_COLOR"""
    p[0] = {"type": AST.COLOR, "value": p[1]}


def p_logical_operator(p):
    """logical_operator : AND
    | OR"""
    p[0] = p[1]


# Error rule for syntax errors
def p_error(p):
    raise ElementQueryLanguageParseException(f"Syntax error in input!\n{p}")


parser = yacc.yacc()


def parse(eql_query: str):
    return parser.parse(eql_query)
