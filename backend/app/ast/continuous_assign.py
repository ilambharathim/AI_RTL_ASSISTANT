"""
Continuous assignment AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class ContinuousAssign(ASTNode):

    target: str

    expression: str

    def __init__(
        self,
        target: str,
        expression: str,
    ):

        object.__setattr__(
            self,
            "kind",
            "ContinuousAssign",
        )

        object.__setattr__(
            self,
            "target",
            target,
        )

        object.__setattr__(
            self,
            "expression",
            expression,
        )
