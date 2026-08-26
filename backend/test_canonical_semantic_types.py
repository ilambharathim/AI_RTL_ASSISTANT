from app.ast.expression import (
    IdentifierExpression,
    BinaryExpression,
)

from app.semantics.semantic_model import SemanticModel
from app.semantics.types.rtl.rtl_type import RTLType
from app.semantics.passes.expression_type_checker import (
    ExpressionTypeChecker,
)


def test_expression_checker_uses_canonical_rtl_type():
    model = SemanticModel()

    model.set_semantic_type(
        "a",
        RTLType(
            name="logic",
            width=8,
            signed=False,
            packed=False,
        ),
    )

    result = ExpressionTypeChecker().infer(
        IdentifierExpression("a"),
        model,
    )

    assert result["type"] == "logic"
    assert result["width"] == 8
    assert result["signed"] is False


def test_expression_checker_uses_canonical_signed_type():
    model = SemanticModel()

    model.set_semantic_type(
        "a",
        RTLType(
            name="logic signed",
            width=16,
            signed=True,
            packed=True,
        ),
    )

    result = ExpressionTypeChecker().infer(
        IdentifierExpression("a"),
        model,
    )

    assert result["type"] == "logic signed"
    assert result["width"] == 16
    assert result["signed"] is True


def test_binary_expression_uses_canonical_types():
    model = SemanticModel()

    model.set_semantic_type(
        "a",
        RTLType(
            name="logic",
            width=8,
            signed=False,
        ),
    )

    model.set_semantic_type(
        "b",
        RTLType(
            name="logic signed",
            width=16,
            signed=True,
        ),
    )

    expression = BinaryExpression(
        "+",
        IdentifierExpression("a"),
        IdentifierExpression("b"),
    )

    result = ExpressionTypeChecker().infer(
        expression,
        model,
    )

    assert result["width"] == 16
    assert result["signed"] is True


def test_legacy_types_remain_supported():
    model = SemanticModel()

    model.types["a"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    result = ExpressionTypeChecker().infer(
        IdentifierExpression("a"),
        model,
    )

    assert result["type"] == "logic"
    assert result["width"] == 8
    assert result["signed"] is False
