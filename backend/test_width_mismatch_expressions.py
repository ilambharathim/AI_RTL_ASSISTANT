from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    ProceduralAssignment,
)

from app.ast.expression import (
    IdentifierExpression,
    BinaryExpression,
    UnaryExpression,
)

from app.semantics.semantic_model import SemanticModel
from app.semantics.types.rtl.rtl_type import RTLType

from app.diagnostics.rules.width_mismatch import (
    WidthMismatchRule,
)


def make_model(tree):
    model = SemanticModel()

    model.types["a"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    model.types["b"] = {
        "type": "logic",
        "width": 16,
        "signed": False,
    }

    model.types["c"] = {
        "type": "logic",
        "width": 16,
        "signed": False,
    }

    model.syntax_tree = tree

    return model


def test_binary_expression_width_mismatch():

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
                            "+",
                            IdentifierExpression("b"),
                            IdentifierExpression("c"),
                        ),
                    ),
                ),
            ),
        ),
    )

    model = make_model(tree)

    diagnostics = WidthMismatchRule().run(
        model,
    )

    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]

    assert diagnostic.code == "RIVA3001"

    assert diagnostic.message == (
        "Width mismatch: "
        "a (8 bits) <- "
        "expression (16 bits)"
    )


def test_unary_expression_width_mismatch():

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
                        expression=UnaryExpression(
                            "-",
                            IdentifierExpression("b"),
                        ),
                    ),
                ),
            ),
        ),
    )

    model = make_model(tree)

    diagnostics = WidthMismatchRule().run(
        model,
    )

    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]

    assert diagnostic.code == "RIVA3001"

    assert diagnostic.message == (
        "Width mismatch: "
        "a (8 bits) <- "
        "expression (16 bits)"
    )


def test_binary_expression_matching_width_has_no_diagnostic():

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
                            "+",
                            IdentifierExpression("b"),
                            IdentifierExpression("c"),
                        ),
                    ),
                ),
            ),
        ),
    )

    model = make_model(tree)

    model.types["b"]["width"] = 8
    model.types["c"]["width"] = 8

    diagnostics = WidthMismatchRule().run(
        model,
    )

    assert diagnostics == []

def test_canonical_semantic_type_width_is_used():
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
    model.syntax_tree = tree

    model.set_semantic_type(
        "a",
        RTLType(
            name="logic",
            width=8,
            signed=False,
            packed=False,
        ),
    )

    model.set_semantic_type(
        "b",
        RTLType(
            name="logic",
            width=16,
            signed=False,
            packed=False,
        ),
    )

    diagnostics = WidthMismatchRule().run(model)

    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]

    assert diagnostic.code == "RIVA3001"

    assert diagnostic.message == (
        "Width mismatch: "
        "a (8 bits) <- "
        "b (16 bits)"
    )
