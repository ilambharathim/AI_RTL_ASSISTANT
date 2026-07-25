"""
Section node for the RIVA generic specification AST.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.ast.ast_node import ASTNode


@dataclass(init=False)
class SectionNode(ASTNode):
    """
    Represents an explicit section header and its ordered entries.
    """

    name: str = ""
    entries: list[ASTNode] = field(default_factory=list)

    def __init__(
        self,
        name: str,
        line: int = 0,
        column: int = 0,
        source_file: str = "",
    ) -> None:
        if not isinstance(name, str):
            raise TypeError("name must be a string.")

        if not name.strip():
            raise ValueError("name must not be empty.")

        super().__init__(
            node_type="SECTION",
            line=line,
            column=column,
            source_file=source_file,
        )

        self.name = name
        self.entries = []

    def add_entry(self, entry: ASTNode) -> None:
        """
        Add a validated section entry while preserving source order.
        """

        if not isinstance(entry, ASTNode):
            raise TypeError("entry must be an ASTNode.")

        if isinstance(entry, SectionNode):
            raise TypeError("nested sections are not supported by this AST.")

        self.entries.append(entry)
        self.add_child(entry)
