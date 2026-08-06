"""
Parameter declaration AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class ParameterDeclaration(ASTNode):

    name: str

    value: ASTNode

    def __init__(
        self,
        name: str,
        value: ASTNode,
    ):

        object.__setattr__(
            self,
            "kind",
            "ParameterDeclaration",
        )

        object.__setattr__(
            self,
            "name",
            name,
        )

        object.__setattr__(
            self,
            "value",
            value,
        )
