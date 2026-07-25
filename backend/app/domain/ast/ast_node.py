"""
Base AST Node
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ASTNode:
    """
    Base class for every AST node.
    """

    node_type: str
    line: int = 0
    column: int = 0
    children: List["ASTNode"] = field(default_factory=list)

    def add_child(self, node: "ASTNode"):
        self.children.append(node)

    def child_count(self):
        return len(self.children)
