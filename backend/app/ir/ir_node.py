"""
Base Typed IR node.

Every IR object derives from IRNode.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class IRNode:

    #
    # Kind of IR node
    #
    kind: str

    #
    # Source AST node
    #
    ast = None

    #
    # Semantic type
    #
    semantic_type = None

    #
    # Bit width
    #
    width = None

    #
    # Compile-time constant
    #
    constant = None

    #
    # Source location
    #
    location = None
