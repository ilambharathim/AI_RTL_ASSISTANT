"""
Typed IR module.
Represents one elaborated SystemVerilog module.
"""

from app.ir.ir_node import IRNode


class IRModule(IRNode):

    def __init__(self, name: str = ""):
        super().__init__(kind="IRModule")
        self.name = name
        self.parameters = {}
        self.ports = {}
        self.signals = {}
        self.instances = []
        self.statements = []
