from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    ProceduralAssignment,
)

from app.ast.expression import IdentifierExpression

from app.semantics.semantic_model import SemanticModel

from app.semantics.passes.assignment_compatibility_checker import (
    AssignmentCompatibilityChecker,
)


def test_assignment_width_mismatch():

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
                        expression=IdentifierExpression("b"),
                    ),
                ),
            ),
        ),
    )

    model = SemanticModel()

    #
    # Pretend previous semantic passes already inferred widths.
    #
    model.types["a"] = {
        "width": 8,
    }

    model.types["b"] = {
        "width": 4,
    }

    AssignmentCompatibilityChecker().check(
        tree,
        model,
    )

    assert len(model.diagnostics) == 1

    diag = model.diagnostics[0]

    assert diag["kind"] == "WidthMismatch"
    assert diag["lhs"] == "a"
    assert diag["rhs"] == "b"
    assert diag["lhs_width"] == 8
    assert diag["rhs_width"] == 4
