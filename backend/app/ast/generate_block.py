"""
Generate block AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class GenerateBlock(ASTNode):

    members: tuple

    def __init__(
        self,
        members,
    ):

        object.__setattr__(
            self,
            "kind",
            "GenerateBlock",
        )

        object.__setattr__(
            self,
            "members",
            tuple(members),
        )

