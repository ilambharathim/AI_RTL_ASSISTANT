"""
Generic Worklist Solver.
"""

from collections import deque

from app.analysis.dataflow.dataflow_result import (
    DataFlowResult,
)


class WorklistSolver:

    def solve(
        self,
        cfg,
        analysis,
    ):

        result = DataFlowResult()

        worklist = deque(
            cfg.blocks,
        )

        for block in cfg.blocks:

            result.in_sets[block.id] = (
                analysis.initial()
            )

            result.out_sets[block.id] = (
                analysis.initial()
            )

        while worklist:

            block = worklist.popleft()

            if analysis.forward:

                predecessors = [

                    result.out_sets[
                        predecessor.id
                    ]

                    for predecessor in block.predecessors

                ]

            else:

                predecessors = [

                    result.in_sets[
                        successor.id
                    ]

                    for successor in block.successors

                ]

            incoming = analysis.meet(
                predecessors,
            )

            outgoing = analysis.transfer(
                block,
                incoming,
            )

            if analysis.forward:

                if outgoing != result.out_sets[block.id]:

                    result.in_sets[block.id] = incoming

                    result.out_sets[block.id] = outgoing

                    for successor in block.successors:

                        worklist.append(
                            successor,
                        )

            else:

                if outgoing != result.in_sets[block.id]:

                    result.out_sets[block.id] = incoming

                    result.in_sets[block.id] = outgoing

                    for predecessor in block.predecessors:

                        worklist.append(
                            predecessor,
                        )

        return result
