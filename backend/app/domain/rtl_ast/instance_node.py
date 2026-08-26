from dataclasses import dataclass, field

from .rtl_node import RTLNode


@dataclass(slots=True)
class InstanceNode(RTLNode):
    """
    Represents one instantiated RTL module.
    """

    module_name: str = ""

    instance_name: str = ""

    parameter_overrides: list[RTLNode] = field(
        default_factory=list,
    )

    connections: list[RTLNode] = field(
        default_factory=list,
    )
