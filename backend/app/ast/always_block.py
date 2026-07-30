"""
Always block AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class AlwaysBlock(ASTNode):

    block_type: str

    sensitivity: str

    statements: tuple[ASTNode, ...]

    def __init__(
        self,
        block_type: str,
        sensitivity: str,
        statements: tuple[ASTNode, ...],
    ):

        object.__setattr__(
            self,
            "kind",
            "AlwaysBlock",
        )

        object.__setattr__(
            self,
            "block_type",
            block_type,
        )

        object.__setattr__(
            self,
            "sensitivity",
            sensitivity,
        )

        object.__setattr__(
            self,
            "statements",
            statements,
        )
