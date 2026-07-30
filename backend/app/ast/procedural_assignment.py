"""
Procedural assignment AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class ProceduralAssignment(ASTNode):

    target: str

    operator: str

    expression: str

    def __init__(
        self,
        target: str,
        operator: str,
        expression: str,
    ):

        object.__setattr__(
            self,
            "kind",
            "ProceduralAssignment",
        )

        object.__setattr__(
            self,
            "target",
            target,
        )

        object.__setattr__(
            self,
            "operator",
            operator,
        )

        object.__setattr__(
            self,
            "expression",
            expression,
        )
