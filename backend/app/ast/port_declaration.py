"""
Port declaration AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class PortDeclaration(ASTNode):

    name: str

    def __init__(
        self,
        name: str,
    ):

        object.__setattr__(
            self,
            "kind",
            "PortDeclaration",
        )

        object.__setattr__(
            self,
            "name",
            name,
        )
