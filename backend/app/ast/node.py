"""
Base immutable AST node for RIVA.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ASTNode:
    """
    Root of all AST nodes.
    """

    kind: str
