"""
Module port connection AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class PortConnection(ASTNode):

    port_name: str

    expression: ASTNode

    def __init__(
        self,
        port_name,
        expression,
    ):

        object.__setattr__(
            self,
            "kind",
            "PortConnection",
        )

        object.__setattr__(
            self,
            "port_name",
            port_name,
        )

        object.__setattr__(
            self,
            "expression",
            expression,
        )

        object.__setattr__(
            self,
            "location",
            None,
        )

