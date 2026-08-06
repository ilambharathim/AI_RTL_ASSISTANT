"""
Resolved module instance.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class ResolvedInstance:

    instance_name: str

    module_name: str

    module: object

    connections: tuple = ()

    parameter_overrides: tuple = ()

