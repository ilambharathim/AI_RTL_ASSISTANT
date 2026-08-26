from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
    UnaryExpression,
    BinaryExpression,
)

from app.semantics.semantic_model import SemanticModel
from app.semantics.passes.expression_type_checker import (
    ExpressionTypeChecker,
)


def make_model():
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

    return model


def test_unary_plus_preserves_operand_type():

    model = make_model()

    expression = UnaryExpression(
        "+",
        IdentifierExpression("a"),
    )

    result = ExpressionTypeChecker().infer(
        expression,
        model,
    )

    assert result["type"] == "logic"
    assert result["width"] == 8
    assert result["signed"] is False


def test_unary_minus_preserves_operand_type():

    model = make_model()

    expression = UnaryExpression(
        "-",
        IdentifierExpression("b"),
    )

    result = ExpressionTypeChecker().infer(
        expression,
        model,
    )

    assert result["type"] == "logic"
    assert result["width"] == 16
    assert result["signed"] is True


def test_unary_bitwise_not_preserves_operand_type():

    model = make_model()

    expression = UnaryExpression(
        "~",
        IdentifierExpression("a"),
    )

    result = ExpressionTypeChecker().infer(
        expression,
        model,
    )

    assert result["type"] == "logic"
    assert result["width"] == 8
    assert result["signed"] is False


def test_unsupported_unary_operator_returns_none():

    model = make_model()

    expression = UnaryExpression(
        "invalid",
        IdentifierExpression("a"),
    )

    result = ExpressionTypeChecker().infer(
        expression,
        model,
    )

    assert result is None


def test_nested_unary_expression():

    model = make_model()

    expression = UnaryExpression(
        "-",
        UnaryExpression(
            "~",
            IdentifierExpression("b"),
        ),
    )

    result = ExpressionTypeChecker().infer(
        expression,
        model,
    )

    assert result["width"] == 16
    assert result["signed"] is True


def test_binary_expression_width_uses_maximum():

    model = make_model()

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


def test_binary_expression_signedness_propagates():

    model = make_model()

    expression = BinaryExpression(
        "+",
        IdentifierExpression("a"),
        IdentifierExpression("b"),
    )

    result = ExpressionTypeChecker().infer(
        expression,
        model,
    )

    assert result["signed"] is True


def test_literal_is_signed_32_bit_integer():

    model = SemanticModel()

    result = ExpressionTypeChecker().infer(
        LiteralExpression("42"),
        model,
    )

    assert result["type"] == "int"
    assert result["width"] == 32
    assert result["signed"] is True


def test_sized_hex_literal():

    model = SemanticModel()

    result = ExpressionTypeChecker().infer(
        LiteralExpression("8'hFF"),
        model,
    )

    assert result["type"] == "int"
    assert result["width"] == 8
    assert result["signed"] is False


def test_sized_signed_hex_literal():

    model = SemanticModel()

    result = ExpressionTypeChecker().infer(
        LiteralExpression("8'shFF"),
        model,
    )

    assert result["type"] == "int"
    assert result["width"] == 8
    assert result["signed"] is True


def test_sized_binary_literal():

    model = SemanticModel()

    result = ExpressionTypeChecker().infer(
        LiteralExpression("4'b1010"),
        model,
    )

    assert result["width"] == 4
    assert result["signed"] is False


def test_sized_signed_binary_literal():

    model = SemanticModel()

    result = ExpressionTypeChecker().infer(
        LiteralExpression("4'sb1010"),
        model,
    )

    assert result["width"] == 4
    assert result["signed"] is True


def test_unsized_decimal_literal_remains_32_bit_signed():

    model = SemanticModel()

    result = ExpressionTypeChecker().infer(
        LiteralExpression("42"),
        model,
    )

    assert result["width"] == 32
    assert result["signed"] is True
