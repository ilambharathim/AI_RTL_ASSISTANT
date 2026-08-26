from dataclasses import dataclass

from app.domain.rtl_ast.rtl_node import RTLNode


@dataclass(slots=True)
class PortNode(RTLNode):
    """
    RTL module port.
    """

    name: str = ""

    direction: str = ""

    datatype: str = "logic"

    width: int = 1

    signed: bool = False
