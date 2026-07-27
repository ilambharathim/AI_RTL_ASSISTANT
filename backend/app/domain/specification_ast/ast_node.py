"""
Base node contract for the RIVA generic specification AST.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ASTNode:
    """
    Base class for every generic specification AST node.

    Line and column values use zero for synthetic or manually constructed
    nodes. Nodes produced by the parser will use one-based source locations.
    """

    node_type: str
    line: int = 0
    column: int = 0
    source_file: str = ""
    children: list[ASTNode] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.node_type, str) or not self.node_type:
            raise ValueError("node_type must be a non-empty string.")

        if not isinstance(self.line, int) or self.line < 0:
            raise ValueError("line must be an integer greater than or equal to 0.")

        if not isinstance(self.column, int) or self.column < 0:
            raise ValueError(
                "column must be an integer greater than or equal to 0."
            )

        if not isinstance(self.source_file, str):
            raise TypeError("source_file must be a string.")

    def add_child(self, node: ASTNode) -> None:
        """
        Add a validated child node while preserving source order.
        """

        if not isinstance(node, ASTNode):
            raise TypeError("child must be an ASTNode.")

        self.children.append(node)

    def child_count(self) -> int:
        """
        Return the number of direct child nodes.
        """

        return len(self.children)
