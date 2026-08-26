"""
Constant propagation.
"""

from app.optimization.base_pass import OptimizationPass
from app.optimization.model.pass_result import PassResult


class ConstantPropagation(
    OptimizationPass,
):

    name = "ConstantPropagation"

    def run(
        self,
        semantic_model,
        context,
    ):

        result = PassResult()

        if not hasattr(semantic_model, "elaboration") or not semantic_model.elaboration or not hasattr(semantic_model.elaboration, "netlist"):
            return result

        constants = getattr(semantic_model, "constant_values", {})
        modules = getattr(semantic_model.elaboration.netlist, "modules", {})
        for module in modules.values():
            if hasattr(module, "instances"):
                for instance in module.instances:
                    if hasattr(instance, "nets"):
                        for net in instance.nets:
                            if hasattr(net, "signal") and net.signal in constants and net.constant != constants[net.signal]:
                                net.constant = constants[net.signal]
                                result.changed = True

        return result
