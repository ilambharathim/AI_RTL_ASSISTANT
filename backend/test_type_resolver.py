from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    PackedRange,
)

from app.ast.expression import LiteralExpression

from app.semantics.semantic_model import SemanticModel
from app.semantics.type_checking.type_resolver import TypeResolver


def test_type_resolver_populates_legacy_and_canonical_types():
    tree = CompilationUnit(
        declarations=(
            ModuleDeclaration(
                name="top",
                ports=(),
                members=(
                    SignalDeclaration(
                        signal_type="logic",
                        packed_range=PackedRange(
                            LiteralExpression("7"),
                            LiteralExpression("0"),
                        ),
                        name="a",
                    ),
                ),
            ),
        ),
    )

    model = SemanticModel()

    TypeResolver().resolve(
        tree,
        model,
    )

    assert "a" in model.types
    assert model.types["a"]["type"] == "logic"
    assert model.types["a"]["packed_range"] is not None
    assert model.types["a"]["width"] == 8
    assert model.types["a"]["signed"] is False

    semantic_type = model.get_semantic_type("a")

    assert semantic_type is not None
    assert semantic_type.name == "logic"
    assert semantic_type.width == 8
    assert semantic_type.signed is False
    assert semantic_type.packed is True


def test_type_resolver_handles_unsigned_scalar():
    tree = CompilationUnit(
        declarations=(
            ModuleDeclaration(
                name="top",
                ports=(),
                members=(
                    SignalDeclaration(
                        signal_type="logic",
                        packed_range=None,
                        name="a",
                    ),
                ),
            ),
        ),
    )

    model = SemanticModel()

    TypeResolver().resolve(
        tree,
        model,
    )

    semantic_type = model.get_semantic_type("a")

    assert semantic_type.width == 1
    assert semantic_type.signed is False
    assert semantic_type.packed is False


def test_type_resolver_handles_signed_packed_signal():
    tree = CompilationUnit(
        declarations=(
            ModuleDeclaration(
                name="top",
                ports=(),
                members=(
                    SignalDeclaration(
                        signal_type="logic signed",
                        packed_range=PackedRange(
                            LiteralExpression("15"),
                            LiteralExpression("0"),
                        ),
                        name="a",
                    ),
                ),
            ),
        ),
    )

    model = SemanticModel()

    TypeResolver().resolve(
        tree,
        model,
    )

    semantic_type = model.get_semantic_type("a")

    assert semantic_type.name == "logic signed"
    assert semantic_type.width == 16
    assert semantic_type.signed is True
    assert semantic_type.packed is True
