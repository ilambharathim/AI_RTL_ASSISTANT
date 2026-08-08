from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    PackedRange,
)

from app.ast.expression import LiteralExpression

from app.semantics.semantic_model import SemanticModel
from app.semantics.passes.width_inference import WidthInference


def test_width_inference():

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

    WidthInference().infer(
        tree,
        model,
    )

    assert model.types["a"]["width"] == 8
