"""
Compilation unit AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class CompilationUnit(ASTNode):

    declarations: tuple[ASTNode, ...]

    def __init__(
        self,
        declarations: tuple[ASTNode, ...],
    ):

        object.__setattr__(
            self,
            "kind",
            "CompilationUnit",
        )

        object.__setattr__(
            self,
            "declarations",
            declarations,
        )
