from app.ir import (
    Net,
    Netlist,
    NetlistInstance,
    NetlistModule,
)

from app.optimization.optimizer import Optimizer
from app.semantics.semantic_model import SemanticModel
from app.semantics.symbols.symbol_info import SymbolInfo


model = SemanticModel()

model.symbols["clk"] = SymbolInfo(
    name="clk",
    symbol_type="logic",
)

model.symbols["unused"] = SymbolInfo(
    name="unused",
    symbol_type="logic",
)

netlist = Netlist()

module = NetlistModule(
    name="top",
)

instance = NetlistInstance(
    name="u0",
    module="child",
)

instance.nets.append(

    Net(

        port="clk",

        signal="clk",

    )

)

module.instances.append(
    instance,
)

netlist.modules["top"] = module

model.elaboration.netlist = netlist

Optimizer().optimize(
    model,
)

assert "clk" in model.symbols

assert "unused" not in model.symbols

print("Typed DeadSignalElimination test passed.")

