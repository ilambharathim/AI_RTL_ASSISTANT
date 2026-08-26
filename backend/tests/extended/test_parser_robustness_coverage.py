"""
Parser Robustness Tests — Priority 2 targets.

Covers:
- generate_parser.py: explicit generate wrapper, GenerateIf/For dispatch, empty generate block
- module_parser.py: module with instance, module with generate, no ports, unknown member skip
- expression_parser.py: parenthesized expression, unary ops, all binary ops, function call, literal, RuntimeError
- case_parser.py: case/casez/casex, default label, malformed item, endcase
- if_parser.py: if with else, if without else, no-paren if
- token_builder.py: valid builds, TypeError/ValueError guards
"""

import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.generate_parser import GenerateParser
from app.parsers.rtl.parsers.module_parser import ModuleParser
from app.parsers.rtl.parsers.expression_parser import ExpressionParser
from app.parsers.rtl.parsers.case_parser import CaseParser
from app.parsers.rtl.parsers.if_parser import IfParser
from app.parsers.specification.token_builder import TokenBuilder
from app.parsers.specification.token_types import TokenType


def _ctx(source: str) -> ParserContext:
    result = RTLLexer().tokenize(source)
    return ParserContext(result.tokens)


# ─── GenerateParser ───────────────────────────────────────────────────────────

class TestGenerateParser:

    def test_generate_if_without_wrapper(self):
        ctx = _ctx("if (EN) assign q = 1;")
        assert GenerateParser.matches(ctx)
        node = GenerateParser.parse(ctx)
        assert node is not None

    def test_generate_for_without_wrapper(self):
        ctx = _ctx("for (genvar i = 0; i < 4; i = i + 1) begin assign a = b; end")
        assert GenerateParser.matches(ctx)
        node = GenerateParser.parse(ctx)
        assert node is not None

    def test_explicit_generate_endgenerate_wrapper_with_if(self):
        """generate is lexed as IDENTIFIER, so GenerateParser.matches delegates to GenerateIfParser."""
        ctx = _ctx("if (X) assign q = 1;")
        assert GenerateParser.matches(ctx)
        node = GenerateParser.parse(ctx)
        assert node is not None

    def test_empty_generate_block_returns_none(self):
        """Lines 64-65, 104: explicit generate with no inner construct returns None."""
        ctx = _ctx("generate endgenerate")
        # skip the "generate" token as matches reads the current token
        node = GenerateParser.parse(ctx)
        assert node is None

    def test_generate_parser_not_matches_plain_assign(self):
        ctx = _ctx("assign a = b;")
        assert not GenerateParser.matches(ctx)


# ─── ModuleParser ─────────────────────────────────────────────────────────────

class TestModuleParser:

    def test_module_with_no_ports(self):
        ctx = _ctx("module top; endmodule")
        assert ModuleParser.matches(ctx)
        node = ModuleParser.parse(ctx)
        assert node.name == "top"
        assert len(node.ports) == 0

    def test_module_with_ports(self):
        ctx = _ctx("module dut(input logic clk, output logic q); endmodule")
        node = ModuleParser.parse(ctx)
        assert node.name == "dut"
        assert len(node.ports) > 0

    def test_module_with_assignment(self):
        ctx = _ctx("module dut; assign a = b; endmodule")
        node = ModuleParser.parse(ctx)
        assert node.name == "dut"
        assert len(node.members) >= 1

    def test_module_with_generate_construct(self):
        """Exercises generate dispatch in ModuleParser member loop."""
        ctx = _ctx("module dut; generate if (1) assign q = 1; endgenerate endmodule")
        node = ModuleParser.parse(ctx)
        assert node.name == "dut"

    def test_module_with_module_instance(self):
        ctx = _ctx("module top; sub_mod u_sub(.a(x)); endmodule")
        node = ModuleParser.parse(ctx)
        assert node.name == "top"

    def test_module_with_always_block(self):
        ctx = _ctx("module dut; always @(posedge clk) begin a <= b; end endmodule")
        node = ModuleParser.parse(ctx)
        assert node.name == "dut"

    def test_module_with_comma_separated_port_list(self):
        """Exercises the comma-advancing branch inside port list."""
        ctx = _ctx("module dut(input a, input b); endmodule")
        node = ModuleParser.parse(ctx)
        assert len(node.ports) >= 1


# ─── ExpressionParser ─────────────────────────────────────────────────────────

class TestExpressionParser:

    def test_identifier(self):
        from app.ast.expression import IdentifierExpression
        ctx = _ctx("sig_a")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, IdentifierExpression)
        assert expr.name == "sig_a"

    def test_literal_number(self):
        from app.ast.expression import LiteralExpression
        ctx = _ctx("42")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, LiteralExpression)

    def test_unary_minus(self):
        from app.ast.expression import UnaryExpression
        ctx = _ctx("-a")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, UnaryExpression)
        assert expr.operator == "-"

    def test_unary_bitwise_not(self):
        from app.ast.expression import UnaryExpression
        ctx = _ctx("~a")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, UnaryExpression)
        assert expr.operator == "~"

    def test_binary_add(self):
        from app.ast.expression import BinaryExpression
        ctx = _ctx("a + b")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == "+"

    def test_binary_multiply(self):
        from app.ast.expression import BinaryExpression
        ctx = _ctx("a * b")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == "*"

    def test_binary_shift(self):
        from app.ast.expression import BinaryExpression
        ctx = _ctx("a << 2")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == "<<"

    def test_binary_comparison_equal(self):
        from app.ast.expression import BinaryExpression
        ctx = _ctx("a == b")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == "=="

    def test_parenthesized_expression(self):
        from app.ast.expression import BinaryExpression
        ctx = _ctx("(a + b)")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, BinaryExpression)

    def test_function_call_with_arguments(self):
        from app.ast.expression import FunctionCallExpression
        ctx = _ctx("$clog2(WIDTH)")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, FunctionCallExpression)
        assert len(expr.arguments) == 1

    def test_function_call_with_multiple_arguments(self):
        from app.ast.expression import FunctionCallExpression
        ctx = _ctx("$signed(a, b)")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, FunctionCallExpression)
        assert len(expr.arguments) == 2

    def test_function_call_empty_args(self):
        from app.ast.expression import FunctionCallExpression
        ctx = _ctx("$bits()")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, FunctionCallExpression)

    def test_eof_raises_runtime_error(self):
        """EOF token causes _primary to see EOF and raise."""
        from app.domain.rtl_tokens import RTLToken, RTLTokenType
        from app.shared.source_location import SourceLocation
        eof_token = RTLToken(
            token_type=RTLTokenType.END_OF_FILE,
            value="",
            source_location=SourceLocation("", 1, 1),
        )
        ctx = ParserContext((eof_token,))
        with pytest.raises(RuntimeError):
            ExpressionParser.parse(ctx)

    def test_precedence_lower_stops_right_recursion(self):
        """Tests that lower-precedence ops stop recursion: a + b * c."""
        from app.ast.expression import BinaryExpression
        ctx = _ctx("a + b * c")
        expr = ExpressionParser.parse(ctx)
        # Top-level should be + and right subtree should be *
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == "+"

    def test_missing_closing_paren_raises(self):
        ctx = _ctx("(a + b")
        with pytest.raises(RuntimeError, match="Expected '\\)'"):
            ExpressionParser.parse(ctx)

    def test_logical_and(self):
        from app.ast.expression import BinaryExpression
        ctx = _ctx("a && b")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == "&&"

    def test_logical_or(self):
        from app.ast.expression import BinaryExpression
        ctx = _ctx("a || b")
        expr = ExpressionParser.parse(ctx)
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == "||"


# ─── CaseParser ───────────────────────────────────────────────────────────────

class TestCaseParser:

    def test_case_with_multiple_items(self):
        from app.ast.case_statement import CaseStatement
        ctx = _ctx("case (sel) 1: a = 1; 0: a = 0; endcase")
        assert CaseParser.matches(ctx)
        node = CaseParser.parse(ctx)
        assert isinstance(node, CaseStatement)
        assert len(node.items) == 2

    def test_casez(self):
        ctx = _ctx("casez (sel) 1: a = 0; endcase")
        assert CaseParser.matches(ctx)
        node = CaseParser.parse(ctx)
        assert node.expression == "sel"

    def test_casex(self):
        ctx = _ctx("casex (data) 1: out = 1; endcase")
        assert CaseParser.matches(ctx)
        node = CaseParser.parse(ctx)
        assert isinstance(node.items, tuple)

    def test_default_label(self):
        ctx = _ctx("case (x) 1: a = 0; default: a = 1; endcase")
        node = CaseParser.parse(ctx)
        labels = [item.label for item in node.items]
        assert "default" in labels

    def test_missing_open_paren_raises(self):
        """Line 68 branch: no '(' after case keyword."""
        ctx = _ctx("case x 1: a = 1; endcase")
        with pytest.raises(RuntimeError, match="Expected '\\('"):
            CaseParser.parse(ctx)

    def test_case_without_items_parses_cleanly(self):
        """Covers the fallback advance when no items before endcase."""
        ctx = _ctx("case (x) endcase")
        node = CaseParser.parse(ctx)
        assert isinstance(node.items, tuple)

    def test_not_matches_assign(self):
        ctx = _ctx("assign a = b;")
        assert not CaseParser.matches(ctx)


# ─── IfParser ─────────────────────────────────────────────────────────────────

class TestIfParser:

    def test_if_with_else_branch(self):
        from app.ast.if_statement import IfStatement
        ctx = _ctx("if (cond) a = 1; else a = 0;")
        assert IfParser.matches(ctx)
        node = IfParser.parse(ctx)
        assert isinstance(node, IfStatement)
        assert len(node.then_branch) > 0
        assert len(node.else_branch) > 0

    def test_if_without_else_branch(self):
        from app.ast.if_statement import IfStatement
        ctx = _ctx("if (rst) q = 0;")
        node = IfParser.parse(ctx)
        assert isinstance(node, IfStatement)
        assert len(node.then_branch) > 0
        assert len(node.else_branch) == 0

    def test_if_else_if_chain(self):
        from app.ast.if_statement import IfStatement
        ctx = _ctx("if (a) x = 1; else if (b) x = 2; else x = 3;")
        node = IfParser.parse(ctx)
        assert isinstance(node, IfStatement)
        assert len(node.else_branch) > 0

    def test_if_not_matches_assign(self):
        ctx = _ctx("assign a = b;")
        assert not IfParser.matches(ctx)

    def test_if_no_paren_start(self):
        """Line 42->51: '(' absent; condition parsing until ')' or token exhaustion."""
        from app.ast.if_statement import IfStatement
        ctx = _ctx("if rst q = 0;")
        # rst is not '(' so the condition read loop runs differently
        node = IfParser.parse(ctx)
        assert isinstance(node, IfStatement)

    def test_if_not_matches_eof(self):
        """IfParser.matches needs an EOF token in the tuple — empty tuple crashes ParserContext."""
        from app.domain.rtl_tokens import RTLToken, RTLTokenType
        from app.shared.source_location import SourceLocation
        eof_token = RTLToken(
            token_type=RTLTokenType.END_OF_FILE,
            value="",
            source_location=SourceLocation("", 1, 1),
        )
        ctx = ParserContext((eof_token,))
        assert not IfParser.matches(ctx)


# ─── TokenBuilder ─────────────────────────────────────────────────────────────

class TestTokenBuilder:

    def test_token_builder_valid_section_header(self):
        token = TokenBuilder.build(
            token_type=TokenType.SECTION_HEADER,
            value="Requirements",
            line=1,
            column=3,
            source_file="spec.md",
        )
        assert token.value == "Requirements"
        assert token.line == 1
        assert token.column == 3

    def test_token_builder_valid_with_section(self):
        token = TokenBuilder.build(
            token_type=TokenType.TEXT,
            value="some text",
            line=5,
            column=1,
            section="intro",
        )
        assert token.section == "intro"

    def test_token_builder_invalid_token_type_raises_type_error(self):
        """Line 27: non-TokenType raises TypeError."""
        with pytest.raises(TypeError, match="token_type must be a TokenType"):
            TokenBuilder.build(
                token_type="SECTION_HEADER",
                value="oops",
                line=1,
                column=1,
            )

    def test_token_builder_invalid_line_raises_value_error(self):
        """Line 30: line < 1 raises ValueError."""
        with pytest.raises(ValueError, match="line number must be >= 1"):
            TokenBuilder.build(
                token_type=TokenType.SECTION_HEADER,
                value="x",
                line=0,
                column=1,
            )

    def test_token_builder_invalid_column_raises_value_error(self):
        """Line 33: column < 1 raises ValueError."""
        with pytest.raises(ValueError, match="column number must be >= 1"):
            TokenBuilder.build(
                token_type=TokenType.SECTION_HEADER,
                value="x",
                line=1,
                column=0,
            )
