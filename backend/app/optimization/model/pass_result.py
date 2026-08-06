"""
Optimization pass result.
"""

from dataclasses import dataclass


@dataclass(slots=True)

class PassResult:

    changed: bool = False

    nodes_removed: int = 0

    symbols_removed: int = 0

    instances_removed: int = 0

