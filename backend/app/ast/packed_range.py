"""
Packed range AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class PackedRange(ASTNode):

    left: ASTNode

    right: ASTNode

    def __init__(
        self,
        left,
        right,
    ):

        object.__setattr__(
            self,
            "kind",
            "PackedRange",
        )

        object.__setattr__(
            self,
            "left",
            left,
        )

        object.__setattr__(
            self,
            "right",
            right,
        )

