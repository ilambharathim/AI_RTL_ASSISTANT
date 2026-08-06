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
            "name",
            name,
        )


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
            "value",
            value,
        )


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
            "operator",
            operator,
        )

        object.__setattr__(
            self,
            "operand",
            operand,
        )


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
            "function_name",
            function_name,
        )

        object.__setattr__(
            self,
            "arguments",
            arguments,
        )
