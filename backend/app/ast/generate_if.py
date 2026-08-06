"""
Generate-if AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class GenerateIf(ASTNode):

    condition: ASTNode

    true_members: tuple

    false_members: tuple

    def __init__(
        self,
        condition,
        true_members,
        false_members=(),
    ):

        object.__setattr__(
            self,
            "kind",
            "GenerateIf",
        )

        object.__setattr__(
            self,
            "condition",
            condition,
        )

        object.__setattr__(
            self,
            "true_members",
            tuple(true_members),
        )

        object.__setattr__(
            self,
            "false_members",
            tuple(false_members),
        )

