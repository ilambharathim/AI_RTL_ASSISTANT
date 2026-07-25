"""
Section Node
"""

from dataclasses import dataclass, field

from app.domain.ast.ast_node import ASTNode


@dataclass
class SectionNode(ASTNode):

    name: str = ""
    entries: list = field(default_factory=list)

    def __init__(self, name: str):
        super().__init__(node_type="SECTION")
        self.name = name
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)
        self.add_child(entry)
