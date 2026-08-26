"""
Typed IR statements.
"""

from app.ir.ir_node import IRNode


class IRStatement(IRNode):

    def __init__(self, kind: str = "IRStatement"):
        super().__init__(kind=kind)


class IRAssignment(IRStatement):

    def __init__(self, target: str, expression, blocking: bool = True):
        super().__init__(kind="IRAssignment")
        self.target = target
        self.expression = expression
        self.blocking = blocking


class IRIf(IRStatement):

    def __init__(self, condition, then_branch, else_branch=None):
        super().__init__(kind="IRIf")
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class IRBlock(IRStatement):

    def __init__(self, statements=None):
        super().__init__(kind="IRBlock")
        self.statements = list(statements or [])


class IRAlways(IRStatement):

    def __init__(self, block_type, sensitivity, body):
        super().__init__(kind="IRAlways")
        self.block_type = block_type
        self.sensitivity = sensitivity
        self.body = body
