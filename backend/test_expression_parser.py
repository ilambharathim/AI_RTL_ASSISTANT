from app.ast.expression import (
    BinaryExpression,
    IdentifierExpression,
)

from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.expression_parser import ExpressionParser

lexer = RTLLexer()

tokens = lexer.tokenize("a+b*c")

context = ParserContext(tokens.tokens)

expr = ExpressionParser.parse(context)

assert isinstance(expr, BinaryExpression)

assert expr.operator == "+"

assert isinstance(
    expr.left,
    IdentifierExpression,
)

assert expr.left.name == "a"

assert isinstance(
    expr.right,
    BinaryExpression,
)

assert expr.right.operator == "*"

assert expr.right.left.name == "b"

assert expr.right.right.name == "c"

print("Binary expression precedence test passed.")
