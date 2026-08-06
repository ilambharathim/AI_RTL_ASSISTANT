"""
Typed IR statements.
"""

from dataclasses import dataclass, field

from app.ir.ir_node import IRNode


@dataclass(slots=True)
class IRStatement(IRNode):

    def __init__(self):

        super().__init__(
            kind="IRStatement",
        )


@dataclass(slots=True)
class IRAssignment(IRStatement):

    target: str = ""

    expression = None

    blocking: bool = True

    def __init__(
        self,
        target,
        expression,
        blocking=True,
    ):

        super().__init__()

        self.kind = "IRAssignment"

        self.target = target

        self.expression = expression

        self.blocking = blocking


@dataclass(slots=True)
class IRIf(IRStatement):

    condition = None

    then_branch = None

    else_branch = None

    def __init__(
        self,
        condition,
        then_branch,
        else_branch=None,
    ):

        super().__init__()

        self.kind = "IRIf"

        self.condition = condition

        self.then_branch = then_branch

        self.else_branch = else_branch


@dataclass(slots=True)
class IRBlock(IRStatement):

    statements: list = field(
        default_factory=list,
    )

    def __init__(
        self,
        statements=None,
    ):

        super().__init__()

        self.kind = "IRBlock"

        self.statements = list(
            statements or []
        )


@dataclass(slots=True)
class IRAlways(IRStatement):

    block_type: str = ""

    sensitivity: str = ""

    body = None

    def __init__(
        self,
        block_type,
        sensitivity,
        body,
    ):

        super().__init__()

        self.kind = "IRAlways"

        self.block_type = block_type

        self.sensitivity = sensitivity

        self.body = body
