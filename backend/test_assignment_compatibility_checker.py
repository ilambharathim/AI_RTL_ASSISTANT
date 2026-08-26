from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    ProceduralAssignment,
)

from app.ast.expression import (
    IdentifierExpression,
    BinaryExpression,
    LiteralExpression,
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


def test_assignment_width_mismatch_from_binary_expression():

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
                    SignalDeclaration(
                        signal_type="logic",
                        packed_range=None,
                        name="c",
                    ),
                    ProceduralAssignment(
                        target="a",
                        operator="=",
                        expression=BinaryExpression(
                            left=IdentifierExpression("b"),
                            operator="+",
                            right=IdentifierExpression("c"),
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
        "width": 8,
        "signed": False,
    }

    model.types["c"] = {
        "type": "logic",
        "width": 16,
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


def test_assignment_width_mismatch_from_literal_expression():

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
                        expression=LiteralExpression(
                            "42",
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

    AssignmentCompatibilityChecker().check(
        tree,
        model,
    )

    assert len(model.diagnostics) == 1

    diagnostic = model.diagnostics[0]

    assert diagnostic.code == "RIVA3001"
    assert diagnostic.category == "Width"
    assert diagnostic.severity == "warning"


def test_assignment_width_match_from_identifier():

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

    model.types["a"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    model.types["b"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    AssignmentCompatibilityChecker().check(
        tree,
        model,
    )

    assert len(model.diagnostics) == 0


def test_assignment_width_match_from_binary_expression():

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
                    SignalDeclaration(
                        signal_type="logic",
                        packed_range=None,
                        name="c",
                    ),
                    ProceduralAssignment(
                        target="a",
                        operator="=",
                        expression=BinaryExpression(
                            left=IdentifierExpression("b"),
                            operator="+",
                            right=IdentifierExpression("c"),
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
        "width": 8,
        "signed": False,
    }

    model.types["c"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    AssignmentCompatibilityChecker().check(
        tree,
        model,
    )

    assert len(model.diagnostics) == 0
