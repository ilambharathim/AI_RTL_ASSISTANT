from dataclasses import dataclass

from app.domain.rtl_ast.rtl_node import RTLNode


@dataclass(slots=True)
class AssignNode(RTLNode):
    left: str = ""
    right: str = ""
