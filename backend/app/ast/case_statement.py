"""
SystemVerilog case statement AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class CaseItem(ASTNode):

    label: str

    statements: tuple[ASTNode, ...]

    def __init__(
        self,
        label: str,
        statements: tuple[ASTNode, ...],
    ):

        object.__setattr__(
            self,
            "kind",
            "CaseItem",
        )

        object.__setattr__(
            self,
            "label",
            label,
        )

        object.__setattr__(
            self,
            "statements",
            statements,
        )


@dataclass(frozen=True, slots=True)
class CaseStatement(ASTNode):

    expression: str

    items: tuple[CaseItem, ...]

    def __init__(
        self,
        expression: str,
        items: tuple[CaseItem, ...],
    ):

        object.__setattr__(
            self,
            "kind",
            "CaseStatement",
        )

        object.__setattr__(
            self,
            "expression",
            expression,
        )

        object.__setattr__(
            self,
            "items",
            items,
        )
