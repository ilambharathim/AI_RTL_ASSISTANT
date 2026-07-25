"""
Root document node for the RIVA generic specification AST.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.ast.ast_node import ASTNode
from app.domain.ast.section_node import SectionNode


@dataclass(init=False)
class DocumentNode(ASTNode):
    """
    Root node for one parsed specification document.

    ``entries`` contains document-level content that appears before any
    section header. ``sections`` contains explicit document sections.
    ``children`` preserves the order in which all direct nodes were added.
    """

    title: str = ""
    entries: list[ASTNode] = field(default_factory=list)
    sections: list[SectionNode] = field(default_factory=list)

    def __init__(
        self,
        title: str = "",
        line: int = 0,
        column: int = 0,
        source_file: str = "",
    ) -> None:
        if not isinstance(title, str):
            raise TypeError("title must be a string.")

        super().__init__(
            node_type="DOCUMENT",
            line=line,
            column=column,
            source_file=source_file,
        )

        self.title = title
        self.entries = []
        self.sections = []

    def add_entry(self, entry: ASTNode) -> None:
        """
        Add document-level content while preserving source order.
        """

        if not isinstance(entry, ASTNode):
            raise TypeError("entry must be an ASTNode.")

        if isinstance(entry, SectionNode):
            raise TypeError("section nodes must be added with add_section().")

        self.entries.append(entry)
        self.add_child(entry)

    def add_section(self, section: SectionNode) -> None:
        """
        Add a validated section while preserving source order.
        """

        if not isinstance(section, SectionNode):
            raise TypeError("section must be a SectionNode.")

        self.sections.append(section)
        self.add_child(section)
