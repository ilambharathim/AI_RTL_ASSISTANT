"""
Key-value entry node for the RIVA generic specification AST.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.specification_ast.ast_node import ASTNode


@dataclass(init=False)
class KeyValueNode(ASTNode):
    """
    Represents one generic ``key: value`` specification entry.

    Empty values are allowed because semantic validation belongs to a later
    compiler stage. Keys must contain at least one non-whitespace character.
    """

    key: str = ""
    value: str = ""

    def __init__(
        self,
        key: str,
        value: str,
        line: int = 0,
        column: int = 0,
        source_file: str = "",
    ) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be a string.")

        if not key.strip():
            raise ValueError("key must not be empty.")

        if not isinstance(value, str):
            raise TypeError("value must be a string.")

        super().__init__(
            node_type="KEY_VALUE",
            line=line,
            column=column,
            source_file=source_file,
        )

        self.key = key
        self.value = value
