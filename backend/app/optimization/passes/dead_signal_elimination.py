"""
Dead signal elimination pass.
"""

from app.optimization.base_pass import OptimizationPass
from app.optimization.model.pass_result import PassResult


class DeadSignalElimination(
    OptimizationPass,
):

    name = "DeadSignalElimination"

    def run(
        self,
        semantic_model,
        context,
    ):

        result = PassResult()
        elaboration = getattr(semantic_model, "elaboration", None)
        if not elaboration or not hasattr(elaboration, "netlist") or not hasattr(elaboration.netlist, "modules"):
            return result

        used = set()
        for module in elaboration.netlist.modules.values():
            for instance in getattr(module, "instances", []):
                for net in getattr(instance, "nets", []):
                    if getattr(net, "signal", None):
                        used.add(net.signal)

        symbols = getattr(semantic_model, "symbols", {})
        dead = [name for name in list(symbols.keys()) if name not in used]
        for name in dead:
            del symbols[name]
            result.symbols_removed += 1
            result.changed = True

        return result
