from dataclasses import dataclass

from app.domain.rtl_ast.rtl_node import RTLNode


@dataclass(slots=True)
class AssignNode(RTLNode):
    """
    Represents a continuous assignment.
    """

    target: str = ""

    expression: str = ""
