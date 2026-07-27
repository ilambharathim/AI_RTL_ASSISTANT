from dataclasses import dataclass

from .rtl_node import RTLNode


@dataclass(slots=True)
class InstanceNode(RTLNode):
    """Represents one instantiated RTL module."""

    module_name: str = ""
    instance_name: str = ""
