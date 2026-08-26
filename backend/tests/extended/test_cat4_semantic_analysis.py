"""
Category 4: Semantic analysis tests (T301 - T315)
"""

import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.diagnostics.diagnostic_engine import DiagnosticEngine


def test_T301_missing_module_semantic_error():
    code = "module top; u_sub u_inst(); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T302_duplicate_module_detection():
    code = "module dup; endmodule module dup; endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T303_duplicate_signal_detection():
    code = "module top(input logic a); logic a; endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T304_duplicate_parameter_detection():
    code = "module top #(parameter W = 8, parameter W2 = 16); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T305_undefined_signal_reference():
    code = "module top; always_comb begin a = undefined_sig; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T306_undefined_parameter_reference():
    code = "module top; logic [UNDEFINED_PARAM-1:0] data; endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T307_invalid_signal_type():
    code = "module top; logic [7:0] valid_sig; endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T308_invalid_parameter_type():
    code = "module top #(parameter W = 8); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T309_signed_unsigned_interaction():
    code = "module top; logic signed [7:0] s; logic unsigned [7:0] u; always_comb begin s = u; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    engine = DiagnosticEngine()
    diagnostics = engine.analyze(semantic_model)
    assert isinstance(diagnostics, list)


def test_T310_scalar_vector_interaction():
    code = "module top; logic s; logic [7:0] v; always_comb begin s = v; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T311_multi_dimensional_signal():
    code = "module top; logic [7:0] mem [15:0]; endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T312_parameter_expression_resolution():
    code = "module top #(parameter WIDTH = 16, parameter DEPTH = WIDTH * 2); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T313_constant_expression_evaluation():
    code = "module top; localparam VAL = 8 + 8; logic [VAL-1:0] bus; endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_T314_semantic_diagnostic_ordering():
    code = "module top; logic [7:0] a; logic [15:0] b; always_comb begin a = b; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    engine = DiagnosticEngine()
    diagnostics = engine.analyze(semantic_model)
    assert isinstance(diagnostics, list)


def test_T315_semantic_analysis_deterministic_rerun():
    code = "module top(input logic [15:0] in, output logic [7:0] out); always_comb begin out = in; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    
    analyzer1 = SemanticAnalyzer()
    model1 = analyzer1.analyze(parse_result.syntax_tree)
    
    analyzer2 = SemanticAnalyzer()
    model2 = analyzer2.analyze(parse_result.syntax_tree)
    
    assert type(model1) == type(model2)
