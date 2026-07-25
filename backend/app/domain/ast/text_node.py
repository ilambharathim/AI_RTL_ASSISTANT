"""
Free-form text node for the RIVA generic specification AST.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.ast.ast_node import ASTNode


@dataclass(init=False)
class TextNode(ASTNode):
    """
    Represents one free-form text line in a specification document.

    Interpretation of the text belongs to later semantic-analysis stages.
    """

    value: str = ""

    def __init__(
        self,
        value: str,
        line: int = 0,
        column: int = 0,
        source_file: str = "",
    ) -> None:
        if not isinstance(value, str):
            raise TypeError("value must be a string.")

        if not value.strip():
            raise ValueError("value must not be empty.")

        super().__init__(
            node_type="TEXT",
            line=line,
            column=column,
            source_file=source_file,
        )

        self.value = value
