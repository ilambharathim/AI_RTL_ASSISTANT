"""
Typed IR expressions.
"""

from dataclasses import dataclass, field

from app.ir.ir_node import IRNode


@dataclass(slots=True)
class IRExpression(IRNode):

    def __init__(self):

        super().__init__(
            kind="IRExpression",
        )


@dataclass(slots=True)
class IRIdentifier(IRExpression):

    name: str = ""

    def __init__(
        self,
        name: str,
    ):

        super().__init__()

        self.kind = "IRIdentifier"

        self.name = name


@dataclass(slots=True)
class IRLiteral(IRExpression):

    value: object = None

    def __init__(
        self,
        value,
    ):

        super().__init__()

        self.kind = "IRLiteral"

        self.value = value


@dataclass(slots=True)
class IRUnary(IRExpression):

    operator: str = ""

    operand: IRExpression = None

    def __init__(
        self,
        operator,
        operand,
    ):

        super().__init__()

        self.kind = "IRUnary"

        self.operator = operator

        self.operand = operand


@dataclass(slots=True)
class IRBinary(IRExpression):

    operator: str = ""

    left: IRExpression = None

    right: IRExpression = None

    def __init__(
        self,
        operator,
        left,
        right,
    ):

        super().__init__()

        self.kind = "IRBinary"

        self.operator = operator

        self.left = left

        self.right = right


@dataclass(slots=True)
class IRFunctionCall(IRExpression):

    function_name: str = ""

    arguments: tuple = field(
        default_factory=tuple,
    )

    def __init__(
        self,
        function_name,
        arguments,
    ):

        super().__init__()

        self.kind = "IRFunctionCall"

        self.function_name = function_name

        self.arguments = tuple(
            arguments,
        )
