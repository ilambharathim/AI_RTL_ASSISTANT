from app.ir import (
    Net,
    Netlist,
    NetlistInstance,
    NetlistModule,
)

from app.optimization.optimizer import Optimizer
from app.semantics.semantic_model import SemanticModel


model = SemanticModel()

netlist = Netlist()

module = NetlistModule(
    name="top",
)

dead = NetlistInstance(
    name="dead",
    module="child",
)

dead.nets.append(

    Net(

        port="a",

        signal=None,

    )

)

alive = NetlistInstance(
    name="alive",
    module="child",
)

alive.nets.append(

    Net(

        port="a",

        signal="clk",

    )

)

module.instances.extend(

    [

        dead,

        alive,

    ]

)

netlist.modules["top"] = module

model.elaboration.netlist = netlist

Optimizer().optimize(
    model,
)

assert (

    len(

        model.elaboration.netlist
        .modules["top"]
        .instances

    )

    == 1

)

assert (

    model.elaboration.netlist
    .modules["top"]
    .instances[0]
    .name

    == "alive"

)

print("Typed DeadInstanceElimination test passed.")

