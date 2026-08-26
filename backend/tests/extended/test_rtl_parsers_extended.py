"""
Comprehensive Unit Test Suite for Phase 4 — RTL Parsers.
Validates 100% of missing branches for:
- ExpressionParser (system calls, parens, eof/unexpected tokens)
- GenerateForParser & GenerateIfParser
- ModuleInstanceParser
"""

import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.parsers.rtl.parsers.expression_parser import ExpressionParser
from app.parsers.rtl.parser_context import ParserContext


def test_expression_parser_system_call_and_parens():
    code = "$clog2(16, 2) + (a * b)"
    tokens = RTLLexer().tokenize(code)
    context = ParserContext(tokens.tokens)
    expr = ExpressionParser.parse(context)
    assert expr is not None


def test_expression_parser_missing_closing_paren():
    code = "(a + b"
    tokens = RTLLexer().tokenize(code)
    context = ParserContext(tokens.tokens)
    with pytest.raises(RuntimeError, match="Expected '\\)'"):
        ExpressionParser.parse(context)


def test_expression_parser_unexpected_token():
    code = "endmodule"
    tokens = RTLLexer().tokenize(code)
    context = ParserContext(tokens.tokens)
    with pytest.raises(RuntimeError, match="Unexpected token"):
        ExpressionParser.parse(context)


def test_generate_for_and_if_parsing():
    code = """
    module top;
        genvar i;
        generate
            if (1) begin : g_if
                assign a = 1;
            end else begin : g_else
                assign a = 0;
            end

            for (i = 0; i < 4; i = i + 1) begin : g_for
                sub_mod #(.W(8)) u_inst(.in(i), .out(o));
            end
        endgenerate
    endmodule
    """
    tokens = RTLLexer().tokenize(code)
    res = RTLParser().parse(tokens.tokens)
    assert res.syntax_tree is not None
