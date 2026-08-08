from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
)

from app.semantics.semantic_model import SemanticModel
from app.semantics.passes.signedness_resolver import (
    SignednessResolver,
)


def test_signedness_resolver():

    tree = CompilationUnit(
        declarations=(
            ModuleDeclaration(
                name="top",
                ports=(),
                members=(
                    SignalDeclaration(
                        signal_type="logic signed",
                        packed_range=None,
                        name="a",
                    ),
                    SignalDeclaration(
                        signal_type="logic",
                        packed_range=None,
                        name="b",
                    ),
                ),
            ),
        ),
    )

    model = SemanticModel()

    SignednessResolver().resolve(
        tree,
        model,
    )

    assert model.types["a"]["signed"] is True
    assert model.types["b"]["signed"] is False
