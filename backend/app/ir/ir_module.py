"""
Typed IR module.

Represents one elaborated SystemVerilog module.
"""

from dataclasses import dataclass, field

from app.ir.ir_node import IRNode


@dataclass(slots=True)
class IRModule(IRNode):

    name: str = ""

    parameters: dict = field(
        default_factory=dict,
    )

    ports: dict = field(
        default_factory=dict,
    )

    signals: dict = field(
        default_factory=dict,
    )

    instances: list = field(
        default_factory=list,
    )

    statements: list = field(
        default_factory=list,
    )

    def __init__(
        self,
        name: str,
    ):

        super().__init__(
            kind="IRModule",
        )

        self.name = name

        self.parameters = {}

        self.ports = {}

        self.signals = {}

        self.instances = []

        self.statements = []
