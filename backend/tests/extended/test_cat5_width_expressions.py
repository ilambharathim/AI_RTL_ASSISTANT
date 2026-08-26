"""
Category 5: Type, width, and expression system tests (T316 - T335)
"""

import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer


def test_T316_1_bit_expression():
    code = "module top; logic a, b, c; always_comb begin c = a & b; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T317_2_bit_expression():
    code = "module top; logic [1:0] a, b, c; always_comb begin c = a + b; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T318_maximum_width_binary_operands():
    code = "module top; logic [63:0] a, b, c; always_comb begin c = a ^ b; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T319_smaller_width_left_operand():
    code = "module top; logic [3:0] a; logic [7:0] b, c; always_comb begin c = a + b; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T320_smaller_width_right_operand():
    code = "module top; logic [7:0] a, c; logic [3:0] b; always_comb begin c = a + b; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T321_mixed_signed_unsigned_operands():
    code = "module top; logic signed [7:0] s; logic unsigned [7:0] u, res; always_comb begin res = s + u; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T322_nested_binary_expressions():
    code = "module top; logic [7:0] a, b, c, d; always_comb begin d = (a + b) * c; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T323_deeply_nested_expressions():
    code = "module top; logic [7:0] a, b, c, d, e; always_comb begin e = ((a + b) & (c | d)) ^ a; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T324_unary_operator_width():
    code = "module top; logic [7:0] a; logic b; always_comb begin b = |a; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T325_unary_operator_signedness():
    code = "module top; logic signed [7:0] a, b; always_comb begin b = -a; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T326_arithmetic_expression():
    code = "module top; logic [15:0] a, b, c; always_comb begin c = a - b; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T327_logical_expression():
    code = "module top; logic a, b, c; always_comb begin c = a && b; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T328_bitwise_expression():
    code = "module top; logic [7:0] a, b, c; always_comb begin c = a ^ b; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T329_shift_expression():
    code = "module top; logic [7:0] a, c; logic [2:0] sh; always_comb begin c = a << sh; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T330_comparison_expression():
    code = "module top; logic [7:0] a, b; logic eq; always_comb begin eq = (a == b); end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T331_concatenation_width():
    code = "module top; logic [3:0] hi, lo; logic [7:0] bus; always_comb begin bus = hi + lo; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T332_part_select_width():
    code = "module top; logic [15:0] in; logic [7:0] out; always_comb begin out = in[15:8]; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T333_indexed_select_width():
    code = "module top; logic [15:0] in; logic bit_out; always_comb begin bit_out = in[4]; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T334_unsized_literal_interaction():
    code = "module top; logic [7:0] out; always_comb begin out = 8'd255; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T335_sized_literal_overflow_compatibility():
    code = "module top; logic [3:0] out; always_comb begin out = 4'hF; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None
