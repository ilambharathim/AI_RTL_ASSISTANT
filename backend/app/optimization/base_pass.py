"""
Base optimization pass.
"""

from app.optimization.model.pass_result import PassResult


class OptimizationPass:

    name = "OptimizationPass"

    def run(

        self,

        semantic_model,

        context,

    ) -> PassResult:

        raise NotImplementedError

