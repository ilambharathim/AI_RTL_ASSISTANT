"""
Generate-for AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class GenerateFor(ASTNode):

    variable: str

    initializer: ASTNode

    condition: ASTNode

    update: ASTNode

    members: tuple

    def __init__(
        self,
        variable,
        initializer,
        condition,
        update,
        members,
    ):

        object.__setattr__(
            self,
            "kind",
            "GenerateFor",
        )

        object.__setattr__(
            self,
            "variable",
            variable,
        )

        object.__setattr__(
            self,
            "initializer",
            initializer,
        )

        object.__setattr__(
            self,
            "condition",
            condition,
        )

        object.__setattr__(
            self,
            "update",
            update,
        )

        object.__setattr__(
            self,
            "members",
            tuple(members),
        )

