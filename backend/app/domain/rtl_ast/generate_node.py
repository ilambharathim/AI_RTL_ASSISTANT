from dataclasses import dataclass, field

from app.domain.rtl_ast.rtl_node import RTLNode


@dataclass(slots=True)
class GenerateNode(RTLNode):
    """
    Represents a SystemVerilog generate block.
    """

    label: str = ""
    condition: str | None = None
    generate_type: str = "block"
    body: list[RTLNode] = field(default_factory=list)
