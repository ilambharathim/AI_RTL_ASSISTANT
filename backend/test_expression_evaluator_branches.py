"""
Comprehensive Branch Test Suite for ExpressionEvaluator.
Validates all execution branches: literals, identifiers, unary/binary ops, division by zero, non-integer constants, and unsupported expressions.
"""

import pytest
from app.semantics.passes.expression_evaluator import ExpressionEvaluator
from app.ast.expression import (
    LiteralExpression,
    IdentifierExpression,
    UnaryExpression,
    BinaryExpression,
)


def test_evaluator_literal_expression():
    expr = LiteralExpression(value="16")
    assert ExpressionEvaluator.evaluate(expr) == 16


def test_evaluator_identifier_expression_integer_constant():
    expr = IdentifierExpression(name="WIDTH")
    assert ExpressionEvaluator.evaluate(expr, constants={"WIDTH": 32}) == 32


def test_evaluator_identifier_expression_string_constant():
    expr = IdentifierExpression(name="DEPTH")
    assert ExpressionEvaluator.evaluate(expr, constants={"DEPTH": "64"}) == 64


def test_evaluator_identifier_expression_invalid_string_constant():
    expr = IdentifierExpression(name="BAD")
    # Non-integer constant fallback returns 1
    assert ExpressionEvaluator.evaluate(expr, constants={"BAD": "not_an_int"}) == 1


def test_evaluator_identifier_expression_unknown_fallback():
    expr = IdentifierExpression(name="UNKNOWN_PARAM")
    # Unknown parameter fallback returns 1
    assert ExpressionEvaluator.evaluate(expr, constants={}) == 1


def test_evaluator_unary_expressions():
    operand = LiteralExpression(value="5")
    
    neg_expr = UnaryExpression(operator="-", operand=operand)
    assert ExpressionEvaluator.evaluate(neg_expr) == -5
    
    pos_expr = UnaryExpression(operator="+", operand=operand)
    assert ExpressionEvaluator.evaluate(pos_expr) == 5


def test_evaluator_binary_expressions():
    left = LiteralExpression(value="10")
    right = LiteralExpression(value="2")
    
    add_expr = BinaryExpression(operator="+", left=left, right=right)
    assert ExpressionEvaluator.evaluate(add_expr) == 12
    
    sub_expr = BinaryExpression(operator="-", left=left, right=right)
    assert ExpressionEvaluator.evaluate(sub_expr) == 8
    
    mul_expr = BinaryExpression(operator="*", left=left, right=right)
    assert ExpressionEvaluator.evaluate(mul_expr) == 20
    
    div_expr = BinaryExpression(operator="/", left=left, right=right)
    assert ExpressionEvaluator.evaluate(div_expr) == 5


def test_evaluator_division_by_zero():
    left = LiteralExpression(value="10")
    zero = LiteralExpression(value="0")
    
    div_zero_expr = BinaryExpression(operator="/", left=left, right=zero)
    # Division by zero returns 0 fallback
    assert ExpressionEvaluator.evaluate(div_zero_expr) == 0


def test_evaluator_unsupported_expression_type():
    class CustomUnsupportedExpr:
        pass
        
    with pytest.raises(RuntimeError, match="Unsupported constant expression"):
        ExpressionEvaluator.evaluate(CustomUnsupportedExpr())
