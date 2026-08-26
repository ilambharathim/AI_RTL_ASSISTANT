from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    PortDeclaration,
    SignalDeclaration,
)

from app.ast.module_instance import ModuleInstance
from app.ast.port_connection import PortConnection
from app.ast.expression import IdentifierExpression

from app.semantics.semantic_model import SemanticModel
from app.semantics.symbols.symbol_info import SymbolInfo

from app.elaboration.validation.port_validator import (
    PortValidator,
)

#
# Target module
#
adder = ModuleDeclaration(

    name="adder",

    ports=(

        PortDeclaration(
            direction="input",
            signal_type="logic",
            packed_range=None,
            name="a",
        ),

        PortDeclaration(
            direction="input",
            signal_type="logic",
            packed_range=None,
            name="b",
        ),

    ),

    members=(),

)

#
# Top module
#
top = ModuleDeclaration(

    name="top",

    ports=(),

    members=(

        SignalDeclaration(
            signal_type="logic",
            packed_range=None,
            name="x",
        ),

        ModuleInstance(

            module_name="adder",

            parameter_overrides=(),

            instance_name="u0",

            connections=(

                PortConnection(
                    "a",
                    IdentifierExpression("x"),
                ),

            ),

        ),

    ),

)

tree = CompilationUnit(

    declarations=(

        adder,

        top,

    ),

)

#
# Fake semantic model
#
model = SemanticModel()

model.symbols["x"] = SymbolInfo(
    name="x",
    symbol_type="logic",
    width=1,
)

model.symbols["a"] = SymbolInfo(
    name="a",
    symbol_type="logic",
    width=1,
)

model.symbols["b"] = SymbolInfo(
    name="b",
    symbol_type="logic",
    width=1,
)

errors = PortValidator().validate(
    tree,
    model,
)

assert len(errors) == 1

assert "Missing connection for port 'b'" in errors[0]

print(errors[0])

print("PortValidator test passed.")



def test_port_validator_prefers_canonical_semantic_types():
    from app.semantics.types.rtl.rtl_type import RTLType

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

    top = ModuleDeclaration(
        name="top",
        ports=(),
        members=(
            SignalDeclaration(
                signal_type="logic",
                packed_range=None,
                name="x",
            ),
            ModuleInstance(
                module_name="child",
                instance_name="u0",
                parameter_overrides=(),
                connections=(
                    PortConnection(
                        "a",
                        IdentifierExpression("x"),
                    ),
                ),
            ),
        ),
    )

    tree = CompilationUnit(
        declarations=(
            child,
            top,
        ),
    )

    model = SemanticModel()

    model.set_semantic_type(
        "x",
        RTLType(
            name="logic",
            width=8,
            signed=False,
            packed=False,
        ),
    )

    model.set_semantic_type(
        "a",
        RTLType(
            name="logic",
            width=4,
            signed=False,
            packed=False,
        ),
    )

    errors = PortValidator().validate(
        tree,
        model,
    )

    assert len(errors) == 1

    assert (
        "Width mismatch on port 'a'"
        in errors[0]
    )

    assert "expected 4" in errors[0]
    assert "got 8" in errors[0]
