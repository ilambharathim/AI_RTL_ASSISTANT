from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    ProceduralAssignment,
)

from app.ast.expression import (
    IdentifierExpression,
)

from app.semantics.semantic_model import (
    SemanticModel,
)

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
                        expression=IdentifierExpression(
                            "b",
                        ),
                    ),
                ),
            ),
        ),
    )

    model = SemanticModel()

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

    AssignmentCompatibilityChecker().check(
        tree,
        model,
    )

    assert len(model.diagnostics) == 1

    diagnostic = model.diagnostics[0]

    assert diagnostic.code == "RIVA3001"
    assert diagnostic.category == "Width"
    assert diagnostic.severity == "warning"

    assert diagnostic.message == (
        "Width mismatch: "
        "a (8 bits) <- "
        "b (4 bits)"
    )

    assert diagnostic.explanation == (
        "The destination signal width differs from the "
        "source expression width."
    )

    assert diagnostic.suggestion == (
        "Resize the source or destination, or explicitly "
        "slice or extend the value."
    )
