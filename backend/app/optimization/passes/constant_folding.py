"""
Constant folding pass.
"""

from app.optimization.base_pass import OptimizationPass
from app.optimization.model.pass_result import PassResult


class ConstantFolding(
    OptimizationPass,
):

    name = "ConstantFolding"

    def run(
        self,
        semantic_model,
        context,
    ):

        result = PassResult()
        elaboration = getattr(semantic_model, "elaboration", None)
        if not elaboration or not hasattr(elaboration, "netlist") or not hasattr(elaboration.netlist, "modules"):
            return result

        constants = getattr(semantic_model, "constant_values", {})
        for module in elaboration.netlist.modules.values():
            for instance in getattr(module, "instances", []):
                for net in getattr(instance, "nets", []):
                    if getattr(net, "signal", None) in constants:
                        net.constant = constants[net.signal]
                        result.changed = True

        return result
