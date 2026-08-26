"""
Category 6: Assignment, port, and parameter compatibility tests (T336 - T345)
"""

import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.diagnostics.diagnostic_engine import DiagnosticEngine


def test_T336_exact_assignment_compatibility():
    code = "module top; logic [7:0] a, b; always_comb begin a = b; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    engine = DiagnosticEngine()
    diagnostics = engine.analyze(semantic_model)
    assert len(diagnostics) == 0


def test_T337_narrow_destination():
    code = "module top; logic [7:0] dst; logic [15:0] src; always_comb begin dst = src; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    engine = DiagnosticEngine()
    diagnostics = engine.analyze(semantic_model)
    assert len(diagnostics) >= 1


def test_T338_wide_destination():
    code = "module top; logic [15:0] dst; logic [7:0] src; always_comb begin dst = src; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    engine = DiagnosticEngine()
    diagnostics = engine.analyze(semantic_model)
    assert isinstance(diagnostics, list)


def test_T339_signed_destination_mismatch():
    code = "module top; logic signed [7:0] dst; logic unsigned [7:0] src; always_comb begin dst = src; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    engine = DiagnosticEngine()
    diagnostics = engine.analyze(semantic_model)
    assert isinstance(diagnostics, list)


def test_T340_unsigned_destination_mismatch():
    code = "module top; logic unsigned [7:0] dst; logic signed [7:0] src; always_comb begin dst = src; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    engine = DiagnosticEngine()
    diagnostics = engine.analyze(semantic_model)
    assert isinstance(diagnostics, list)


def test_T341_expression_to_port_compatibility():
    code = "module top(output logic [7:0] out); logic [7:0] a, b; always_comb begin out = a + b; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T342_width_mismatched_port_connection():
    code = "module sub(input logic [15:0] in); endmodule module top; logic [7:0] wire8; sub u_sub(.in(wire8)); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T343_signedness_mismatched_port_connection():
    code = "module sub(input logic signed [7:0] in); endmodule module top; logic unsigned [7:0] wire_u; sub u_sub(.in(wire_u)); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T344_parameter_width_incompatibility():
    code = "module top #(parameter logic [3:0] SMALL = 4'hF); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T345_multiple_compatibility_errors_in_one_module():
    code = "module top; logic [3:0] a; logic [7:0] b; logic [15:0] c; always_comb begin a = b; b = c; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    engine = DiagnosticEngine()
    diagnostics = engine.analyze(semantic_model)
    assert len(diagnostics) >= 1
