"""
RIVA Optimizer.

Legacy optimization + Typed IR optimization.
"""

from app.optimization.model.optimization_context import (
    OptimizationContext,
)

#
# Legacy passes
#
from app.optimization.passes.constant_propagation import ConstantPropagation
from app.optimization.passes.constant_folding import ConstantFolding
from app.optimization.passes.dead_signal_elimination import DeadSignalElimination
from app.optimization.passes.dead_instance_elimination import DeadInstanceElimination

#
# Typed IR passes
#
from app.optimization.typed_ir.typed_constant_propagation import (
    TypedConstantPropagation,
)

from app.optimization.typed_ir.typed_constant_folding import (
    TypedConstantFolding,
)

from app.optimization.typed_ir.typed_dead_assignment_elimination import (
    TypedDeadAssignmentElimination,
)

from app.optimization.typed_ir.typed_control_flow_simplification import (
    TypedControlFlowSimplification,
)


class Optimizer:

    def __init__(self):

        self.legacy_passes = (

            ConstantPropagation(),

            ConstantFolding(),

            DeadSignalElimination(),

            DeadInstanceElimination(),

        )

        self.typed_ir_passes = (

            TypedConstantPropagation(),

            TypedConstantFolding(),

            TypedDeadAssignmentElimination(),

            TypedControlFlowSimplification(),

        )

    def optimize(
        self,
        semantic_model,
    ):

        context = OptimizationContext()

        for compiler_pass in self.legacy_passes:

            result = compiler_pass.run(
                semantic_model,
                context,
            )

            context.statistics[
                compiler_pass.name
            ] = result

            if result.changed:

                context.changed = True

        for compiler_pass in self.typed_ir_passes:

            result = compiler_pass.run(
                semantic_model,
                context,
            )

            context.statistics[
                compiler_pass.name
            ] = result

            if result.changed:

                context.changed = True

        semantic_model.optimization_context = context

        return semantic_model
