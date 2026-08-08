from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    ProceduralAssignment,
)

from app.ast.expression import IdentifierExpression

from app.semantics.semantic_model import SemanticModel
from app.semantics.passes.implicit_net_detector import (
    ImplicitNetDetector,
)


def test_implicit_net_detector():

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
                    ProceduralAssignment(
                        target="a",
                        operator="=",
                        expression=IdentifierExpression("missing"),
                    ),
                ),
            ),
        ),
    )

    diagnostics = ImplicitNetDetector().detect(
        tree,
        SemanticModel(),
    )

    assert diagnostics == [
        "Implicit net 'missing'."
    ]


def test_declared_signal_is_not_implicit():

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
                    ProceduralAssignment(
                        target="a",
                        operator="=",
                        expression=IdentifierExpression("a"),
                    ),
                ),
            ),
        ),
    )

    diagnostics = ImplicitNetDetector().detect(
        tree,
        SemanticModel(),
    )

    assert diagnostics == []
