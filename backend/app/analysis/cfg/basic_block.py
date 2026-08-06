"""
Basic Block.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class BasicBlock:

    id: int

    statements: list = field(
        default_factory=list,
    )

    predecessors: list = field(
        default_factory=list,
    )

    successors: list = field(
        default_factory=list,
    )

    def connect(
        self,
        block,
    ):

        if block not in self.successors:

            self.successors.append(
                block,
            )

        if self not in block.predecessors:

            block.predecessors.append(
                self,
            )
