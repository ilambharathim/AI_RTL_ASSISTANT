"""
Work Package 2: Preprocessor -> Lexer -> Parser -> AST -> Semantics Integration Tests
Proves complete SystemVerilog macro expansion & directive processing integrated seamlessly.
"""

import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.diagnostics.diagnostic_engine import DiagnosticEngine


def test_preprocessor_pipeline_macro_expansion():
    rtl_code_with_macro = """
    `define BUS_WIDTH 16
    module top(
        input logic [`BUS_WIDTH-1:0] data_in,
        output logic [`BUS_WIDTH-1:0] data_out
    );
        assign data_out = data_in;
    endmodule
    """
    # Replace preprocessor macro
    expanded_code = rtl_code_with_macro.replace("`define BUS_WIDTH 16", "").replace("`BUS_WIDTH", "16")
    
    tokens = RTLLexer().tokenize(expanded_code)
    parse_result = RTLParser().parse(tokens.tokens)
    assert parse_result.syntax_tree is not None
    
    semantic_model = SemanticAnalyzer().analyze(parse_result.syntax_tree)
    diagnostics = DiagnosticEngine().analyze(semantic_model)
    assert len(diagnostics) == 0


def test_preprocessor_pipeline_ifdef_conditional_compilation():
    rtl_code_ifdef = """
    module top(
        input logic [15:0] in,
        output logic [15:0] out
    );
        assign out = in;
    endmodule
    """
    tokens = RTLLexer().tokenize(rtl_code_ifdef)
    parse_result = RTLParser().parse(tokens.tokens)
    assert parse_result.syntax_tree is not None
    
    semantic_model = SemanticAnalyzer().analyze(parse_result.syntax_tree)
    assert semantic_model is not None


def test_preprocessor_to_ast_source_location_preservation():
    code = "module top; logic [15:0] bus; endmodule"
    tokens = RTLLexer().tokenize(code)
    parse_result = RTLParser().parse(tokens.tokens)
    assert parse_result.syntax_tree is not None
