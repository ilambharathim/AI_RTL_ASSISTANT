"""
Module declaration AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class ModuleDeclaration(ASTNode):

    name: str

    ports: tuple[ASTNode, ...]

    members: tuple[ASTNode, ...]

    def __init__(
        self,
        name: str,
        ports: tuple[ASTNode, ...],
        members: tuple[ASTNode, ...],
    ):

        object.__setattr__(
            self,
            "kind",
            "ModuleDeclaration",
        )

        object.__setattr__(
            self,
            "name",
            name,
        )

        object.__setattr__(
            self,
            "ports",
            ports,
        )

        object.__setattr__(
            self,
            "members",
            members,
        )
