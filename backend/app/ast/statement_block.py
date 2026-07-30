"""
SystemVerilog begin/end statement block AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class StatementBlock(ASTNode):

    statements: tuple[ASTNode, ...]

    def __init__(
        self,
        statements: tuple[ASTNode, ...],
    ):

        object.__setattr__(
            self,
            "kind",
            "StatementBlock",
        )

        object.__setattr__(
            self,
            "statements",
            statements,
        )
