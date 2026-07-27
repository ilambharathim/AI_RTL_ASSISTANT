from dataclasses import dataclass

from app.domain.rtl_ast.rtl_node import RTLNode


@dataclass(slots=True)
class SignalNode(RTLNode):
    """
    Represents an internal RTL signal declaration.
    """

    name: str = ""
    datatype: str = "logic"
    width: int = 1
    signed: bool = False
