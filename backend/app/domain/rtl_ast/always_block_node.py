from dataclasses import dataclass, field

from app.domain.rtl_ast.rtl_node import RTLNode


@dataclass(slots=True)
class AlwaysBlockNode(RTLNode):
    """
    Represents an always block in the RTL AST.
    """

    block_type: str = ""

    sensitivity: str = ""

    statements: list[RTLNode] = field(
        default_factory=list,
    )
