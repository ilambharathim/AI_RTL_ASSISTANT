"""
Dead instance elimination pass.
"""

from app.optimization.base_pass import OptimizationPass
from app.optimization.model.pass_result import PassResult


class DeadInstanceElimination(
    OptimizationPass,
):

    name = "DeadInstanceElimination"

    def run(
        self,
        semantic_model,
        context,
    ):

        result = PassResult()
        elaboration = getattr(semantic_model, "elaboration", None)
        if not elaboration or not hasattr(elaboration, "netlist") or not hasattr(elaboration.netlist, "modules"):
            return result

        for module in elaboration.netlist.modules.values():
            alive_instances = []
            for instance in getattr(module, "instances", []):
                is_connected = any(getattr(net, "signal", None) is not None for net in getattr(instance, "nets", []))
                if is_connected:
                    alive_instances.append(instance)
                else:
                    result.instances_removed += 1
                    result.changed = True
            module.instances = alive_instances

        return result
