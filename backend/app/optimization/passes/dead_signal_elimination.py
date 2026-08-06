"""
Dead signal elimination.
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

        used = set()

        for module in (
            semantic_model.elaboration.netlist.modules.values()
        ):

            for instance in module.instances:

                for net in instance.nets:

                    if net.signal is not None:

                        used.add(
                            net.signal,
                        )

        dead = [

            name

            for name in semantic_model.symbols

            if name not in used

        ]

        for name in dead:

            del semantic_model.symbols[name]

        result.symbols_removed = len(dead)

        result.changed = (

            len(dead) > 0

        )

        return result

