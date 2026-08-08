from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    ProceduralAssignment,
)

from app.ast.expression import (
    IdentifierExpression,
    BinaryExpression,
)

from app.semantics.semantic_model import SemanticModel

from app.semantics.passes.implicit_net_detector import (
    ImplicitNetDetector,
)


def test_implicit_net_inside_binary_expression():

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
                    SignalDeclaration(
                        signal_type="logic",
                        packed_range=None,
                        name="b",
                    ),
                    ProceduralAssignment(
                        target="a",
                        operator="=",
                        expression=BinaryExpression(
                            "+",
                            IdentifierExpression("b"),
                            IdentifierExpression("missing"),
                        ),
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


if __name__ == "__main__":
    test_implicit_net_inside_binary_expression()
    print("Implicit net expression test passed.")
