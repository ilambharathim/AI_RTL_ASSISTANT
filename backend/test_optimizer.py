from app.ir import (
    Net,
    Netlist,
    NetlistModule,
    NetlistInstance,
)

from app.optimization.optimizer import Optimizer
from app.semantics.semantic_model import SemanticModel


model = SemanticModel()

model.constant_values["WIDTH"] = 8

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

        port="WIDTH",

        signal="WIDTH",

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

assert (
    model.elaboration.netlist
    .modules["top"]
    .instances[0]
    .nets[0]
    .constant
    == 8
)

print("Typed ConstantPropagation test passed.")

