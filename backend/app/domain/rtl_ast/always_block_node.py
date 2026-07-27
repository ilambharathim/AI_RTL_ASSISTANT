from dataclasses import dataclass

from app.domain.rtl_ast.rtl_node import RTLNode


@dataclass(slots=True)
class AlwaysBlockNode(RTLNode):
    """
    Represents an always block in the RTL AST.
    """

    sensitivity: str = ""
