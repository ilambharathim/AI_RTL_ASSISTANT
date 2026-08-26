from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    PackedRange,
)

from app.ast.expression import LiteralExpression

from app.semantics.semantic_model import SemanticModel
from app.semantics.type_checking.type_resolver import TypeResolver
from app.semantics.width.width_inference import WidthInference


def test_width_inference_updates_legacy_and_canonical_types():

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

    WidthInference().infer(
        tree,
        model,
    )

    assert model.types["a"]["width"] == 8

    semantic_type = model.get_semantic_type("a")

    assert semantic_type is not None
    assert semantic_type.width == 8
    assert semantic_type.signed is False
    assert semantic_type.packed is True
