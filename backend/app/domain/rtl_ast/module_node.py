from dataclasses import dataclass, field

from app.domain.rtl_ast.rtl_node import RTLNode


@dataclass(slots=True)
class ModuleNode(RTLNode):
    """
    Represents one RTL module.
    """

    name: str = ""
    ports: list[str] = field(default_factory=list)
    parameters: list[str] = field(default_factory=list)
