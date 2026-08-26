"""
Focused Unit Tests for Phase 7 — Expression Type Checker.
Tests missing branches in ExpressionTypeChecker:
- Unary expression with None or invalid operator
- FunctionCallExpression infer
- _normalize_semantic_type with None width/signed
- _normalize_type_info with object type_info and dict without width
- Invalid/unknown expression node types
"""

import pytest
from app.ast.expression import (
    UnaryExpression,
    FunctionCallExpression,
    IdentifierExpression,
)
from app.semantics.passes.expression_type_checker import ExpressionTypeChecker
from app.semantics.semantic_model import SemanticModel


def test_expression_type_checker_unary_none_operand():
    checker = ExpressionTypeChecker()
    model = SemanticModel()

    # Unary expression whose operand infers to None (e.g. unknown identifier)
    expr = UnaryExpression(operator="-", operand=IdentifierExpression("unknown_sig"))
    assert checker.infer(expr, model) is None

    # Unary expression with invalid operator
    expr_bad_op = UnaryExpression(operator="*", operand=IdentifierExpression("known_sig"))
    model.types["known_sig"] = {"width": 8, "signed": False}
    assert checker.infer(expr_bad_op, model) is None


def test_expression_type_checker_function_call():
    checker = ExpressionTypeChecker()
    model = SemanticModel()
    fn_call = FunctionCallExpression(function_name="$clog2", arguments=())
    assert checker.infer(fn_call, model) is None


def test_expression_type_checker_normalize_semantic_type_object():
    checker = ExpressionTypeChecker()

    # Object without width -> returns None
    class DummyNoWidth:
        width = None

    assert checker._normalize_semantic_type(DummyNoWidth()) is None

    # Object with width but signed is None -> defaults signed to False
    class DummyNoSigned:
        width = 16
        signed = None
        packed = True
        name = "wire"

    res = checker._normalize_semantic_type(DummyNoSigned())
    assert res["width"] == 16
    assert res["signed"] is False
    assert res["type"] == "wire"


def test_expression_type_checker_normalize_type_info_object_and_dict():
    checker = ExpressionTypeChecker()

    # Object type_info with width
    class DummyTypeObj:
        width = 32
        signed = True
        packed = False
        name = "int"

    res = checker._normalize_type_info(DummyTypeObj())
    assert res["width"] == 32
    assert res["signed"] is True

    # Object type_info without width -> None
    class DummyNoWidthObj:
        width = None

    assert checker._normalize_type_info(DummyNoWidthObj()) is None

    # Dict type_info without width -> None
    assert checker._normalize_type_info({"type": "logic"}) is None


def test_expression_type_checker_unknown_expression():
    checker = ExpressionTypeChecker()
    model = SemanticModel()

    class CustomUnknownExpr:
        pass

    assert checker.infer(CustomUnknownExpr(), model) is None
