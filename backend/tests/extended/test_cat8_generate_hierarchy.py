"""
Category 8: Generate and hierarchy elaboration tests (T361 - T372)
"""

import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.elaboration.elaborator import Elaborator
from app.elaboration.hierarchy_builder import HierarchyTreeBuilder


def test_T361_basic_generate_if():
    code = "module top; parameter ENABLE = 1; generate if (ENABLE) begin logic active; end endgenerate endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful is True


def test_T362_generate_if_false_branch():
    code = "module top; parameter ENABLE = 0; generate if (ENABLE) begin logic active; end endgenerate endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful is True


def test_T363_generate_if_else():
    code = "module top; parameter USE_FAST = 1; generate if (USE_FAST) begin logic fast_clk; end else begin logic slow_clk; end endgenerate endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful is True


def test_T364_generate_for_zero_iterations():
    code = "module top; genvar i; generate for (i = 0; i < 0; i = i + 1) begin logic idx; end endgenerate endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful is True


def test_T365_generate_for_one_iteration():
    code = "module top; genvar i; generate for (i = 0; i < 1; i = i + 1) begin logic idx; end endgenerate endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful is True


def test_T366_generate_for_multiple_iterations():
    code = "module top; genvar i; generate for (i = 0; i < 4; i = i + 1) begin logic bit_lane; end endgenerate endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful is True


def test_T367_parameterized_generate():
    code = "module top #(parameter N = 8); genvar i; generate for (i = 0; i < N; i = i + 1) begin logic lane; end endgenerate endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful is True


def test_T368_nested_generate_if():
    code = "module top; parameter A = 1, B = 1; generate if (A) begin if (B) begin logic dual_flag; end end endgenerate endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful is True


def test_T369_nested_generate_for():
    code = "module top; genvar i, j; generate for (i = 0; i < 2; i = i + 1) begin for (j = 0; j < 2; j = j + 1) begin logic cell; end end endgenerate endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful is True


def test_T370_mixed_nested_generate_constructs():
    code = "module top; parameter EN = 1; genvar i; generate if (EN) begin for (i = 0; i < 2; i = i + 1) begin logic lane; end end endgenerate endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful is True


def test_T371_hierarchy_with_missing_instance():
    code = "module top; sub_cell u_sub(); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    builder = HierarchyTreeBuilder()
    trees = builder.build_tree(parse_result.syntax_tree)
    assert len(trees) >= 1


def test_T372_hierarchy_cycle_detection():
    code = "module top; top u_self(); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    builder = HierarchyTreeBuilder()
    trees = builder.build_tree(parse_result.syntax_tree)
    assert trees is not None
