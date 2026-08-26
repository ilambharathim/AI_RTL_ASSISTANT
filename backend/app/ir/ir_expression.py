"""
Typed IR expressions.
"""

from app.ir.ir_node import IRNode


class IRExpression(IRNode):

    def __init__(self, kind: str = "IRExpression"):
        super().__init__(kind=kind)


class IRIdentifier(IRExpression):

    def __init__(self, name: str):
        super().__init__(kind="IRIdentifier")
        self.name = name


class IRLiteral(IRExpression):

    def __init__(self, value):
        super().__init__(kind="IRLiteral")
        self.value = value


class IRUnary(IRExpression):

    def __init__(self, operator: str, operand):
        super().__init__(kind="IRUnary")
        self.operator = operator
        self.operand = operand


class IRBinary(IRExpression):

    def __init__(self, operator: str, left, right):
        super().__init__(kind="IRBinary")
        self.operator = operator
        self.left = left
        self.right = right


class IRFunctionCall(IRExpression):

    def __init__(self, function_name: str, arguments: tuple):
        super().__init__(kind="IRFunctionCall")
        self.function_name = function_name
        self.arguments = tuple(arguments)
