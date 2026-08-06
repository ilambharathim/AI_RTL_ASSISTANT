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

        constants = semantic_model.constant_values

        for module in (
            semantic_model.elaboration.netlist.modules.values()
        ):

            for instance in module.instances:

                for net in instance.nets:

                    if (
                        net.signal in constants
                        and net.constant != constants[net.signal]
                    ):

                        net.constant = constants[
                            net.signal
                        ]

                        result.changed = True

        return result

