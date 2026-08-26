"""
Focused Unit Tests for Phase 6 — Constant Folding.
Tests UnaryExpression folding, non-literal operands, BinaryExpression non-literal operands, and default node returns.
"""

import pytest
from app.ast.expression import (
    LiteralExpression,
    IdentifierExpression,
    UnaryExpression,
    BinaryExpression,
)
from app.semantics.passes.constant_folding import ConstantFolding


def test_constant_folding_literal():
    folder = ConstantFolding()
    lit = LiteralExpression("42")
    res = folder.fold(lit)
    assert isinstance(res, LiteralExpression)
    assert res.value == "42"


def test_constant_folding_unary_foldable():
    folder = ConstantFolding()
    # -5 -> -5
    expr = UnaryExpression(operator="-", operand=LiteralExpression("5"))
    res = folder.fold(expr)
    assert isinstance(res, LiteralExpression)
    assert res.value == "-5"


def test_constant_folding_unary_non_foldable():
    folder = ConstantFolding()
    # !a -> UnaryExpression("!", IdentifierExpression("a"))
    expr = UnaryExpression(operator="!", operand=IdentifierExpression("a"))
    res = folder.fold(expr)
    assert isinstance(res, UnaryExpression)
    assert res.operator == "!"
    assert isinstance(res.operand, IdentifierExpression)


def test_constant_folding_binary_foldable():
    folder = ConstantFolding()
    # 2 + 3 -> 5
    expr = BinaryExpression(
        left=LiteralExpression("2"),
        operator="+",
        right=LiteralExpression("3"),
    )
    res = folder.fold(expr)
    assert isinstance(res, LiteralExpression)
    assert res.value == "5"


def test_constant_folding_binary_non_foldable():
    folder = ConstantFolding()
    # a + 3 -> BinaryExpression("+", IdentifierExpression("a"), LiteralExpression("3"))
    expr = BinaryExpression(
        left=IdentifierExpression("a"),
        operator="+",
        right=LiteralExpression("3"),
    )
    res = folder.fold(expr)
    assert isinstance(res, BinaryExpression)
    assert isinstance(res.left, IdentifierExpression)
    assert isinstance(res.right, LiteralExpression)


def test_constant_folding_other_node():
    folder = ConstantFolding()
    ident = IdentifierExpression("x")
    assert folder.fold(ident) is ident
    assert folder.fold(None) is None
