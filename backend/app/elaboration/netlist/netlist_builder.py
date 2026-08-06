"""
Netlist Builder.

Builds the typed IR netlist.
"""

from app.ir import (
    Net,
    Netlist,
    NetlistModule,
    NetlistInstance,
)


class NetlistBuilder:

    def build(
        self,
        semantic_model,
    ):

        netlist = Netlist()

        for module_name, graph in (
            semantic_model.elaboration.rtl_graph.items()
        ):

            module = NetlistModule(
                name=module_name,
            )

            for instance in graph["instances"]:

                ir_instance = NetlistInstance(

                    name=instance.instance_name,

                    module=instance.module_name,

                )

                for binding in instance.bindings:

                    signal = None

                    if (
                        binding.expression is not None
                        and hasattr(
                            binding.expression,
                            "name",
                        )
                    ):

                        signal = binding.expression.name

                    ir_instance.nets.append(

                        Net(

                            port=binding.port_name,

                            signal=signal,

                        )

                    )

                module.instances.append(
                    ir_instance,
                )

            netlist.modules[
                module_name
            ] = module

        semantic_model.elaboration.netlist = (
            netlist
        )

