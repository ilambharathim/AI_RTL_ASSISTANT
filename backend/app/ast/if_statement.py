"""
SystemVerilog if statement AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class IfStatement(ASTNode):

    condition: str

    then_branch: tuple[ASTNode, ...]

    else_branch: tuple[ASTNode, ...]

    def __init__(
        self,
        condition: str,
        then_branch: tuple[ASTNode, ...],
        else_branch: tuple[ASTNode, ...],
    ):

        object.__setattr__(
            self,
            "kind",
            "IfStatement",
        )

        object.__setattr__(
            self,
            "condition",
            condition,
        )

        object.__setattr__(
            self,
            "then_branch",
            then_branch,
        )

        object.__setattr__(
            self,
            "else_branch",
            else_branch,
        )
