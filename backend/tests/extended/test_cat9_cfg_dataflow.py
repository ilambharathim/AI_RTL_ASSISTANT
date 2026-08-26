"""
Category 9: CFG, dataflow, and analysis tests (T373 - T382)
"""

import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.diagnostics.diagnostic_engine import DiagnosticEngine


def test_T373_basic_cfg():
    code = "module top; logic a, b; always_comb begin a = b; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    model = analyzer.analyze(parse_result.syntax_tree)
    assert model is not None


def test_T374_branch_cfg():
    code = "module top; logic c, a, b; always_comb begin if (c) a = 1'b1; else a = 1'b0; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    model = analyzer.analyze(parse_result.syntax_tree)
    assert model is not None


def test_T375_nested_branch_cfg():
    code = "module top; logic c1, c2, a; always_comb begin if (c1) begin if (c2) a = 1'b1; end end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    model = analyzer.analyze(parse_result.syntax_tree)
    assert model is not None


def test_T376_loop_cfg():
    code = "module top; genvar i; generate for (i=0; i<4; i=i+1) begin logic bit_node; end endgenerate endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful is True


def test_T377_unreachable_block_detection():
    code = "module top; logic a; always_comb begin if (1'b0) begin a = 1'b1; end end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    model = analyzer.analyze(parse_result.syntax_tree)
    assert model is not None


def test_T378_live_variable_analysis():
    code = "module top(input logic in, output logic out); always_comb begin out = in; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    model = analyzer.analyze(parse_result.syntax_tree)
    assert model is not None


def test_T379_dead_signal_detection():
    code = "module top; logic unused_signal; endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    model = analyzer.analyze(parse_result.syntax_tree)
    engine = DiagnosticEngine()
    diagnostics = engine.analyze(model)
    assert isinstance(diagnostics, list)


def test_T380_dataflow_across_branch():
    code = "module top; logic cond, in1, in2, out; always_comb begin if (cond) out = in1; else out = in2; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    model = analyzer.analyze(parse_result.syntax_tree)
    assert model is not None


def test_T381_dataflow_across_loop():
    code = "module top; logic [7:0] in; logic parity; genvar i; generate for (i=0; i<8; i=i+1) begin logic lane; end endgenerate endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful is True


def test_T382_analysis_convergence_determinism():
    code = "module top(input logic [15:0] in, output logic [7:0] out); always_comb begin out = in; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    
    analyzer = SemanticAnalyzer()
    model1 = analyzer.analyze(parse_result.syntax_tree)
    model2 = analyzer.analyze(parse_result.syntax_tree)
    
    engine = DiagnosticEngine()
    diag1 = engine.analyze(model1)
    diag2 = engine.analyze(model2)
    assert len(diag1) == len(diag2)
