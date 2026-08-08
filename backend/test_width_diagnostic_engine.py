from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    ProceduralAssignment,
)

from app.ast.expression import IdentifierExpression

from app.diagnostics.diagnostic_engine import DiagnosticEngine

from app.semantics.semantic_model import SemanticModel


def test_width_mismatch_flows_through_diagnostic_engine():

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
                        expression=IdentifierExpression(
                            "b",
                        ),
                    ),
                ),
            ),
        ),
    )

    model = SemanticModel()

    model.syntax_tree = tree

    model.types["a"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    model.types["b"] = {
        "type": "logic",
        "width": 4,
        "signed": False,
    }

    diagnostics = DiagnosticEngine().analyze(
        model,
    )

    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]

    assert diagnostic.code == "RIVA3001"
    assert diagnostic.category == "Width"
    assert diagnostic.severity == "warning"

    assert diagnostic.message == (
        "Width mismatch: "
        "a (8 bits) <- "
        "b (4 bits)"
    )
