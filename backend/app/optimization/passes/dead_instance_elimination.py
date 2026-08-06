"""
Dead instance elimination.
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

        for module in (
            semantic_model.elaboration.netlist.modules.values()
        ):

            alive = []

            removed = 0

            for instance in module.instances:

                keep = any(

                    net.signal is not None

                    for net in instance.nets

                )

                if keep:

                    alive.append(
                        instance,
                    )

                else:

                    removed += 1

            module.instances = alive

            result.instances_removed += removed

        result.changed = (

            result.instances_removed > 0

        )

        return result

