"""
Port declaration AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class PortDeclaration(ASTNode):

    direction: str

    signal_type: str

    packed_range: ASTNode | None

    name: str

    def __init__(
        self,
        direction,
        signal_type,
        packed_range,
        name,
    ):

        object.__setattr__(
            self,
            "kind",
            "PortDeclaration",
        )

        object.__setattr__(
            self,
            "direction",
            direction,
        )

        object.__setattr__(
            self,
            "signal_type",
            signal_type,
        )

        object.__setattr__(
            self,
            "packed_range",
            packed_range,
        )

        object.__setattr__(
            self,
            "name",
            name,
        )

