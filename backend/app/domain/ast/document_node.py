"""
Document Node
"""

from dataclasses import dataclass, field

from app.domain.ast.ast_node import ASTNode


@dataclass
class DocumentNode(ASTNode):

    title: str = ""
    sections: list = field(default_factory=list)

    def __init__(self):
        super().__init__(node_type="DOCUMENT")
        self.title = ""
        self.sections = []

    def add_section(self, section):
        self.sections.append(section)
        self.add_child(section)
