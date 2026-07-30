"""
Signal declaration AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class SignalDeclaration(ASTNode):

    signal_type: str

    name: str

    def __init__(
        self,
        signal_type: str,
        name: str,
    ):

        object.__setattr__(
            self,
            "kind",
            "SignalDeclaration",
        )

        object.__setattr__(
            self,
            "signal_type",
            signal_type,
        )

        object.__setattr__(
            self,
            "name",
            name,
        )
