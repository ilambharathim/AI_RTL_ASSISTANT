from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    ProceduralAssignment,
    PackedRange,
)

from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
)

from app.semantics.semantic_analyzer import SemanticAnalyzer


def test_semantic_analyzer_runs_diagnostic_engine():

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
                    SignalDeclaration(
                        signal_type="logic",
                        packed_range=PackedRange(
                            LiteralExpression("3"),
                            LiteralExpression("0"),
                        ),
                        name="b",
                    ),
                    ProceduralAssignment(
                        target="a",
                        operator="=",
                        expression=IdentifierExpression(
                            "b",
                        ),
                    ),
                ),
            ),
        ),
    )

    model = SemanticAnalyzer().analyze(
        tree,
    )

    width_diagnostics = [
        diagnostic
        for diagnostic in model.diagnostics
        if diagnostic.code == "RIVA3001"
    ]

    assert len(width_diagnostics) == 1

    diagnostic = width_diagnostics[0]

    assert diagnostic.category == "Width"
    assert diagnostic.severity == "warning"
