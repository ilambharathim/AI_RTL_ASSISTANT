"""
SystemVerilog expression AST nodes.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class IdentifierExpression(ASTNode):

    name: str

    def __init__(
        self,
        name: str,
    ):

        object.__setattr__(
            self,
            "kind",
            "IdentifierExpression",
        )

        object.__setattr__(
            self,
            "location",
            None,
        )

        object.__setattr__(
            self,
            "name",
            name,
        )

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, IdentifierExpression):
            return self.name == other.name
        return False


@dataclass(frozen=True, slots=True)
class LiteralExpression(ASTNode):

    value: str

    def __init__(
        self,
        value: str,
    ):

        object.__setattr__(
            self,
            "kind",
            "LiteralExpression",
        )

        object.__setattr__(
            self,
            "location",
            None,
        )

        object.__setattr__(
            self,
            "value",
            value,
        )

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return str(self.value) == other
        if isinstance(other, LiteralExpression):
            return str(self.value) == str(other.value)
        return False


@dataclass(frozen=True, slots=True)
class UnaryExpression(ASTNode):

    operator: str

    operand: ASTNode

    def __init__(
        self,
        operator: str,
        operand: ASTNode,
    ):

        object.__setattr__(
            self,
            "kind",
            "UnaryExpression",
        )

        object.__setattr__(
            self,
            "location",
            None,
        )

        object.__setattr__(
            self,
            "operator",
            operator,
        )

        object.__setattr__(
            self,
            "operand",
            operand,
        )

    def __str__(self) -> str:
        return f"{self.operator}{self.operand}"

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return str(self) == other
        if isinstance(other, UnaryExpression):
            return (self.operator, self.operand) == (other.operator, other.operand)
        return False


@dataclass(frozen=True, slots=True)
class BinaryExpression(ASTNode):

    operator: str

    left: ASTNode

    right: ASTNode

    def __init__(
        self,
        operator: str,
        left: ASTNode,
        right: ASTNode,
    ):

        object.__setattr__(
            self,
            "kind",
            "BinaryExpression",
        )

        object.__setattr__(
            self,
            "location",
            None,
        )

        object.__setattr__(
            self,
            "operator",
            operator,
        )

        object.__setattr__(
            self,
            "left",
            left,
        )

        object.__setattr__(
            self,
            "right",
            right,
        )

    def __str__(self) -> str:
        return f"{self.left} {self.operator} {self.right}"

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return str(self) == other
        if isinstance(other, BinaryExpression):
            return (self.operator, self.left, self.right) == (other.operator, other.left, other.right)
        return False


@dataclass(frozen=True, slots=True)
class FunctionCallExpression(ASTNode):

    function_name: str

    arguments: tuple[ASTNode, ...]

    def __init__(
        self,
        function_name: str,
        arguments: tuple[ASTNode, ...],
    ):

        object.__setattr__(
            self,
            "kind",
            "FunctionCallExpression",
        )

        object.__setattr__(
            self,
            "location",
            None,
        )

        object.__setattr__(
            self,
            "function_name",
            function_name,
        )

        object.__setattr__(
            self,
            "arguments",
            arguments,
        )

    def __str__(self) -> str:
        args_str = ", ".join(str(a) for a in self.arguments)
        return f"{self.function_name}({args_str})"

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return str(self) == other
        if isinstance(other, FunctionCallExpression):
            return (self.function_name, self.arguments) == (other.function_name, other.arguments)
        return False
