from app.ast.expression import (
    IdentifierExpression,
    BinaryExpression,
    LiteralExpression,
)

from app.semantics.semantic_model import SemanticModel
from app.semantics.passes.expression_type_checker import (
    ExpressionTypeChecker,
)


def test_binary_expression_uses_max_width():

    model = SemanticModel()

    model.types["a"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    model.types["b"] = {
        "type": "logic",
        "width": 16,
        "signed": False,
    }

    expr = BinaryExpression(
        "+",
        IdentifierExpression("a"),
        IdentifierExpression("b"),
    )

    result = ExpressionTypeChecker().infer(
        expr,
        model,
    )

    assert result["width"] == 16


def test_literal_expression_has_32_bit_width():

    model = SemanticModel()

    result = ExpressionTypeChecker().infer(
        LiteralExpression("42"),
        model,
    )

    assert result["width"] == 32
    assert result["signed"] is True


def test_binary_expression_propagates_signedness():

    model = SemanticModel()

    model.types["a"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    model.types["b"] = {
        "type": "logic",
        "width": 8,
        "signed": True,
    }

    expr = BinaryExpression(
        "+",
        IdentifierExpression("a"),
        IdentifierExpression("b"),
    )

    result = ExpressionTypeChecker().infer(
        expr,
        model,
    )

    assert result["signed"] is True


if __name__ == "__main__":
    test_binary_expression_uses_max_width()
    test_literal_expression_has_32_bit_width()
    test_binary_expression_propagates_signedness()

    print("Expression width semantics test passed.")
