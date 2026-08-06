from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ModuleInstance,
    PortDeclaration,
    PortConnection,
)

from app.ast.expression import IdentifierExpression

from app.semantics.semantic_model import SemanticModel

from app.elaboration.modules.module_resolver import (
    ModuleResolver,
)

from app.elaboration.instances.instance_resolver import (
    InstanceResolver,
)

from app.elaboration.ports.port_binder import (
    PortBinder,
)

from app.elaboration.rtl_graph.rtl_graph_builder import (
    RTLGraphBuilder,
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
        ModuleInstance(
            module_name="child",
            parameter_overrides=(),
            instance_name="u0",
            connections=(
                PortConnection(
                    port_name="clk",
                    expression=IdentifierExpression("clk"),
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

RTLGraphBuilder().build(
    model,
)

graph = model.elaboration.rtl_graph

assert "top" in graph

assert graph["top"]["instances"][0].instance_name == "u0"

assert graph["top"]["instances"][0].module_name == "child"

print("Typed RTLGraphBuilder test passed.")
