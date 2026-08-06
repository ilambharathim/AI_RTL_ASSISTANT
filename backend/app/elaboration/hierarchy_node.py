"""
Hierarchy node.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class HierarchyNode:

    name: str

    module_name: str

    children: list = field(default_factory=list)

