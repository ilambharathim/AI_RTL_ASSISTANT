from app.ast.expression import (
    IdentifierExpression,
    BinaryExpression,
)

from app.semantics.semantic_model import SemanticModel
from app.semantics.passes.expression_type_checker import (
    ExpressionTypeChecker,
)


def test_expression_type_checker():

    model = SemanticModel()

    model.types["a"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    model.types["b"] = {
        "type": "logic",
        "width": 16,
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

    assert result["type"] == "logic"
    assert result["width"] == 16
    assert result["signed"] is True
