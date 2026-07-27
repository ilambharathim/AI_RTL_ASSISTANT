from dataclasses import dataclass

from app.domain.rtl_ast.rtl_node import RTLNode


@dataclass(slots=True)
class ParameterNode(RTLNode):
    """Represents a Verilog/SystemVerilog parameter."""

    name: str = ""
    value: str = ""
