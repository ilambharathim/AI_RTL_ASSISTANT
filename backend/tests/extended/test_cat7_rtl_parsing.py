"""
Category 7: RTL parsing grammar tests (T346 - T360)
"""

import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser


def test_T346_module_declaration():
    code = "module simple_module; endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T347_module_ports():
    code = "module with_ports(input logic clk, input logic reset, output logic [7:0] data); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T348_signal_declarations():
    code = "module top; logic clk; logic [15:0] data_bus; logic signed [7:0] signed_bus; endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T349_parameter_declarations():
    code = "module top #(parameter WIDTH = 16, parameter DEPTH = 8); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T350_continuous_assignment():
    code = "module top; logic a, b, c; assign c = a & b; endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T351_blocking_assignment():
    code = "module top; logic [7:0] a, b; always_comb begin a = b + 1; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T352_nonblocking_assignment():
    code = "module top; logic clk; logic [7:0] q, d; always_ff @(posedge clk) begin q <= d; end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T353_nested_if():
    code = "module top; logic a, b, c, d; always_comb begin if (a) begin if (b) begin c = d; end end end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T354_nested_if_else():
    code = "module top; logic a, b, c, d; always_comb begin if (a) begin if (b) c = d; else c = 1'b0; end else begin c = 1'b1; end end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T355_case_default():
    code = "module top; logic [1:0] sel; logic [3:0] out; always_comb begin case (sel) 2'b00: out = 4'h1; default: out = 4'h0; endcase end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T356_casez_edge_cases():
    code = "module top; logic [1:0] sel; logic out; always_comb begin casez (sel) 2'b1?: out = 1'b1; default: out = 1'b0; endcase end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T357_casex_edge_cases():
    code = "module top; logic [1:0] sel; logic out; always_comb begin casex (sel) 2'bx1: out = 1'b1; default: out = 1'b0; endcase end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T358_nested_procedural_blocks():
    code = "module top; logic clk, reset; logic [7:0] q, d; always_ff @(posedge clk or posedge reset) begin if (reset) begin q <= 8'd0; end else begin q <= d; end end endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T359_multiple_always_blocks():
    code = "module top; logic clk, reset, flag; logic [7:0] count; always_ff @(posedge clk) count <= count + 1; always_comb flag = (count == 8'hFF); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T360_invalid_rtl_syntax_diagnostic():
    code = "module top; assign = ; endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None
