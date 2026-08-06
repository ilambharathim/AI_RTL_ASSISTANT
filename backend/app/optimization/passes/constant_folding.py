"""
Constant folding.
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

        return PassResult()

