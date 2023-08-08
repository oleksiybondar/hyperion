from .parser import parse
from hyperiontf.typing import (
    AST,
    LogicalOp,
    ComparisonOp,
    ElementQueryLanguageBadOperatorException,
)
from hyperiontf.ui.color import Color
import re


def execute(eql_query, element):
    """
    Execute the given EQL (Elements Query Language) query on an element.

    Args:
    - eql_query (str): The EQL query to be executed.
    - element: The element on which the query is to be executed.

    Returns:
    - Result of the evaluation of the EQL query on the given element.
    """
    return evaluate(parse(eql_query), element)


def evaluate(ast_node, element):
    """
    Evaluate the provided AST (Abstract Syntax Tree) node on an element.

    Args:
    - ast_node (dict): The AST node to be evaluated.
    - element: The element on which the AST node is to be evaluated.

    Returns:
    - Result of the evaluation of the AST node on the given element.
    """
    node_type = ast_node["type"]

    if node_type == AST.LOGICAL_EXPRESSION:
        return evaluate_logical_expression(ast_node, element)
    elif node_type == AST.COMPARISON:
        return evaluate_comparison_expression(ast_node, element)
    elif node_type == AST.ELEMENT_CHAIN:
        return element.__resolve_eql_chain__(ast_node["value"])
    else:
        return ast_node["value"]


def evaluate_logical_expression(ast_node, element):
    """
    Evaluate logical expressions (e.g., AND and OR operations) on an element.

    Args:
    - ast_node (dict): The AST node representing the logical expression.
    - element: The element on which the logical expression is to be evaluated.

    Returns:
    - Result of the logical evaluation on the given element.
    """
    if ast_node["operator"] == LogicalOp.OR:
        return evaluate(ast_node["left"], element) or evaluate(
            ast_node["right"], element
        )
    elif ast_node["operator"] == LogicalOp.AND:
        return evaluate(ast_node["left"], element) and evaluate(
            ast_node["right"], element
        )
    else:
        return False


def evaluate_approx_equal(left_operand, right_operand) -> bool:
    """
    Evaluate if the left_operand is approximately equal to the right_operand.

    This method supports approximate equality checks for Color objects and regex pattern matching.
    For Color objects, it checks if the two colors are approximately equal.
    For regex, it checks if one operand is a regex pattern and the other is a string matching this pattern.

    Args:
        left_operand (Color or re.Pattern or str): The left operand for comparison, can be a Color, regex pattern, or string.
        right_operand (Color or re.Pattern or str): The right operand for comparison, can be a Color, regex pattern, or string.

    Returns:
        bool: True if operands are approximately equal or if the string matches the regex pattern, False otherwise.

    Raises:
        ElementQueryLanguageBadOperatorException: If the operands do not conform to the expected types for approximate matching.
    """
    if isinstance(left_operand, Color) and isinstance(right_operand, Color):
        return left_operand.approx_eq(right_operand)
    elif isinstance(left_operand, re.Pattern):
        return re.search(left_operand, right_operand) is not None
    elif isinstance(right_operand, re.Pattern):
        return re.search(right_operand, left_operand) is not None
    else:
        error_msg = (
            "Invalid operands for approximate match (~=): "
            "Operands must be either both Colors or one Regex pattern and one String. "
            f"Received types: {type(left_operand).__name__} and {type(right_operand).__name__}."
        )
        raise ElementQueryLanguageBadOperatorException(error_msg)


COMPARISON_OPERATORS = {
    ComparisonOp.EQUAL: lambda left, right: left == right,
    ComparisonOp.NOTEQUAL: lambda left, right: left != right,
    ComparisonOp.APPROX: evaluate_approx_equal,
    ComparisonOp.GT: lambda left, right: left > right,
    ComparisonOp.LT: lambda left, right: left < right,
    ComparisonOp.GE: lambda left, right: left >= right,
    ComparisonOp.LE: lambda left, right: left <= right,
}


def evaluate_comparison_expression(ast_node, element):
    """
    Evaluate comparison expressions (e.g., ==, !=, >, <, >=, <=, approx) on an element using a mapping of operators
    to their respective evaluation functions.

    Args:
    - ast_node (dict): The AST node representing the comparison expression.
    - element: The element on which the comparison is to be evaluated.

    Returns:
    - Result of the comparison evaluation on the given element or False if the operator is not supported.
    """
    left_operand = evaluate(ast_node["left"], element)
    right_operand = evaluate(ast_node["right"], element)
    operator_func = COMPARISON_OPERATORS.get(ast_node["operator"])

    return operator_func(left_operand, right_operand) if operator_func else False
