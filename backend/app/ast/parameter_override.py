"""
Parameter override AST node.

Example:

#(
    .WIDTH(32),
    .DEPTH(16)
)
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class ParameterOverride(ASTNode):

    name: str

    expression: ASTNode

    def __init__(
        self,
        name,
        expression,
    ):

        object.__setattr__(
            self,
            "kind",
            "ParameterOverride",
        )

        object.__setattr__(
            self,
            "name",
            name,
        )

        object.__setattr__(
            self,
            "expression",
            expression,
        )

