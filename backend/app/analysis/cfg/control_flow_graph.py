"""
Control Flow Graph.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class ControlFlowGraph:

    entry: object = None

    exit: object = None

    blocks: list = field(
        default_factory=list,
    )

    def new_block(
        self,
    ):

        from app.analysis.cfg.basic_block import (
            BasicBlock,
        )

        block = BasicBlock(

            id=len(
                self.blocks,
            ),

        )

        self.blocks.append(
            block,
        )

        return block
