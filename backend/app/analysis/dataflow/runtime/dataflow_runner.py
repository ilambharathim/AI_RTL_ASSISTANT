"""
Runs all data-flow analyses.
"""

from app.analysis.dataflow import (
    WorklistSolver,
)

from app.analysis.dataflow.analyses import (
    LiveVariableAnalysis,
)


class DataFlowRunner:

    def run(
        self,
        elaboration_model,
    ):

        solver = WorklistSolver()

        analysis = LiveVariableAnalysis()

        for module_name, cfg in elaboration_model.cfgs.items():

            elaboration_model.dataflow[module_name] = (

                solver.solve(

                    cfg,

                    analysis,

                )

            )
