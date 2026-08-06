from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ModuleInstance,
    PortConnection,
    PortDeclaration,
    SignalDeclaration,
)
from app.ast.expression import IdentifierExpression

from app.semantics.semantic_model import SemanticModel
from app.semantics.symbols.symbol_info import SymbolInfo

from app.elaboration.modules.module_resolver import (
    ModuleResolver,
)

from app.elaboration.instances.instance_resolver import (
    InstanceResolver,
)
from app.elaboration.ports.port_binder import (
    PortBinder,
)
from app.elaboration.signals.signal_resolver import (
    SignalResolver,
)


child = ModuleDeclaration(
    name="child",
    ports=(
        PortDeclaration(
            direction="input",
            signal_type="logic",
            packed_range=None,
            name="clk",
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
            name="clk",
        ),
        ModuleInstance(
            module_name="child",
            parameter_overrides=(),
            instance_name="u0",
            connections=(
                PortConnection(
                    port_name="clk",
                    expression=IdentifierExpression(
                        "clk",
                    ),
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

model.symbols["clk"] = SymbolInfo(
    name="clk",
    symbol_type="logic",
)

ModuleResolver().resolve(
    tree,
    model,
)

InstanceResolver().resolve(
    tree,
    model,
)

PortBinder().bind(
    model,
)

SignalResolver().resolve(
    model,
)

modules = model.elaboration.elaborated_modules

assert "top" in modules

assert "clk" in modules["top"].signals

print("Typed SignalResolver test passed.")

