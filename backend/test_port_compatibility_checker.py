from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ModuleInstance,
    PortDeclaration,
    SignalDeclaration,
)

from app.ast.port_connection import PortConnection
from app.ast.expression import IdentifierExpression

from app.semantics.semantic_model import SemanticModel
from app.elaboration.validation.port_validator import PortValidator


def test_port_compatibility_unknown_port():

    child = ModuleDeclaration(
        name="child",
        ports=(
            PortDeclaration(
                direction="input",
                signal_type="logic",
                packed_range=None,
                name="a",
            ),
        ),
        members=(),
    )

    parent = ModuleDeclaration(
        name="top",
        ports=(),
        members=(
            SignalDeclaration(
                signal_type="logic",
                packed_range=None,
                name="sig",
            ),

            ModuleInstance(
                module_name="child",
                instance_name="u0",
                parameter_overrides=(),
                connections=(
                    PortConnection(
                        port_name="missing",
                        expression=IdentifierExpression("sig"),
                    ),
                ),
            ),
        ),
    )

    tree = CompilationUnit(
        declarations=(
            child,
            parent,
        ),
    )

    model = SemanticModel()

    diagnostics = PortValidator().validate(
        tree,
        model,
    )

    assert len(diagnostics) == 2

    assert any(
        "Unknown port 'missing'" in diagnostic
        for diagnostic in diagnostics
    )

    assert any(
        "Missing connection for port 'a'" in diagnostic
        for diagnostic in diagnostics
    )


if __name__ == "__main__":
    test_port_compatibility_unknown_port()
    print("Port compatibility test passed.")
