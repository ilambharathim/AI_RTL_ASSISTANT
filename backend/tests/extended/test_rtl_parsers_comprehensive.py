"""
Comprehensive Unit Tests for Phases 3 & 4 — RTL Parsers & Generate Constructs.
Tests all branch paths, matches, success, failure, and error handling for:
- ModuleInstanceParser
- GenerateForParser
- GenerateIfParser
- GenerateParser
- PortConnectionParser
- ParameterOverrideParser
"""

import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.module_instance_parser import ModuleInstanceParser
from app.parsers.rtl.parsers.generate_for_parser import GenerateForParser
from app.parsers.rtl.parsers.generate_if_parser import GenerateIfParser
from app.parsers.rtl.parsers.generate_parser import GenerateParser
from app.parsers.rtl.parsers.port_connection_parser import PortConnectionParser
from app.parsers.rtl.parsers.parameter_override_parser import ParameterOverrideParser
from app.ast import ModuleInstance, GenerateFor, GenerateIf, PortConnection, ParameterOverride


def get_context(code: str) -> ParserContext:
    tokens = RTLLexer().tokenize(code)
    return ParserContext(tokens.tokens)


# ── ModuleInstanceParser ─────────────────────────────────────────────

def test_module_instance_parser_matches():
    assert ModuleInstanceParser.matches(get_context("my_mod inst_1 ( .a(b) );")) is True
    assert ModuleInstanceParser.matches(get_context("my_mod #(.W(8)) inst_1 ( .a(b) );")) is True
    assert ModuleInstanceParser.matches(get_context("")) is False
    assert ModuleInstanceParser.matches(get_context("123")) is False
    assert ModuleInstanceParser.matches(get_context("my_mod")) is False


def test_module_instance_parser_errors():
    with pytest.raises(RuntimeError, match="Expected '\\(' after '#'"):
        ModuleInstanceParser.parse(get_context("my_mod # .W(8) inst_1 ( .a(b) );"))

    with pytest.raises(RuntimeError, match="Expected '\\)' after parameter overrides"):
        ModuleInstanceParser.parse(get_context("my_mod # ( .W(8)"))

    with pytest.raises(RuntimeError, match="Expected instance name"):
        ModuleInstanceParser.parse(get_context("my_mod # ( .W(8) ) 123 ( .a(b) );"))

    with pytest.raises(RuntimeError, match="Expected '\\(' after instance name"):
        ModuleInstanceParser.parse(get_context("my_mod inst_1 .a(b) );"))

    with pytest.raises(RuntimeError, match="Expected '\\)'"):
        ModuleInstanceParser.parse(get_context("my_mod inst_1 ( .a(b)"))

    with pytest.raises(RuntimeError, match=r"Expected ';'"):
        ModuleInstanceParser.parse(get_context("my_mod inst_1 ( .a(b) ) assign a = 1;"))


def test_module_instance_parser_success():
    code = "sub_module #(.PARAM(16)) u_sub (.clk(clk), .rst_n(rst_n));"
    node = ModuleInstanceParser.parse(get_context(code))
    assert isinstance(node, ModuleInstance)
    assert node.module_name == "sub_module"
    assert node.instance_name == "u_sub"
    assert len(node.parameter_overrides) == 1
    assert len(node.connections) == 2


# ── GenerateForParser ────────────────────────────────────────────────

def test_generate_for_parser_matches():
    assert GenerateForParser.matches(get_context("for (i=0; i<4; i=i+1) begin end")) is True
    assert GenerateForParser.matches(get_context("if (1) begin end")) is False
    assert GenerateForParser.matches(get_context("")) is False


def test_generate_for_parser_errors():
    with pytest.raises(RuntimeError, match="Expected '\\(' after for"):
        GenerateForParser.parse(get_context("for i=0; i<4; i=i+1)"))

    with pytest.raises(RuntimeError, match="Expected loop variable"):
        GenerateForParser.parse(get_context("for ( 123 = 0; i<4; i=i+1)"))

    with pytest.raises(RuntimeError, match="Expected '='"):
        GenerateForParser.parse(get_context("for (i 0; i<4; i=i+1)"))

    with pytest.raises(RuntimeError, match="Expected ';' after initializer"):
        GenerateForParser.parse(get_context("for (i = 0 i<4; i=i+1)"))

    with pytest.raises(RuntimeError, match="Expected ';' after condition"):
        GenerateForParser.parse(get_context("for (i = 0; i<4 i=i+1)"))

    with pytest.raises(RuntimeError, match="Expected update variable"):
        GenerateForParser.parse(get_context("for (i = 0; i<4; 123=i+1)"))

    with pytest.raises(RuntimeError, match="Expected '=' in update"):
        GenerateForParser.parse(get_context("for (i = 0; i<4; i + 1)"))


def test_generate_for_parser_success():
    code = "for (genvar i = 0; i < 4; i = i + 1) begin sub_mod u_i (.a(i)); end"
    node = GenerateForParser.parse(get_context(code))
    assert isinstance(node, GenerateFor)
    assert node.variable == "i"


# ── GenerateIfParser ─────────────────────────────────────────────────

def test_generate_if_parser_matches():
    assert GenerateIfParser.matches(get_context("if (ENABLE) begin end")) is True
    assert GenerateIfParser.matches(get_context("for (i=0; i<4; i=i+1)")) is False
    assert GenerateIfParser.matches(get_context("")) is False


def test_generate_if_parser_errors():
    with pytest.raises(RuntimeError, match="Expected '\\(' after if"):
        GenerateIfParser.parse(get_context("if ENABLE) begin end"))

    with pytest.raises(RuntimeError, match="Expected '\\)'"):
        GenerateIfParser.parse(get_context("if (ENABLE begin end"))


def test_generate_if_parser_success():
    code = "if (WIDTH == 8) sub_mod u_8 (.a(b)); else sub_mod u_16 (.a(b));"
    node = GenerateIfParser.parse(get_context(code))
    assert isinstance(node, GenerateIf)


# ── GenerateParser ───────────────────────────────────────────────────

def test_generate_parser_matches():
    assert GenerateParser.matches(get_context("if (1) begin end")) is True
    assert GenerateParser.matches(get_context("for (i=0; i<4; i=i+1)")) is True
    assert GenerateParser.matches(get_context("assign a = b;")) is False
    assert GenerateParser.matches(get_context("")) is False


def test_generate_parser_empty_generate():
    code = "generate unknown_keyword_here endgenerate"
    node = GenerateParser.parse(get_context(code))
    assert node is None


# ── PortConnectionParser ─────────────────────────────────────────────

def test_port_connection_parser_errors():
    with pytest.raises(RuntimeError, match=r"Expected '\.'"):
        PortConnectionParser.parse(get_context("clk(sys_clk)"))

    with pytest.raises(RuntimeError, match="Expected port name"):
        PortConnectionParser.parse(get_context(". 123 (sys_clk)"))

    with pytest.raises(RuntimeError, match="Expected '\\('"):
        PortConnectionParser.parse(get_context(".clk sys_clk)"))

    with pytest.raises(RuntimeError, match="Expected '\\)'"):
        PortConnectionParser.parse(get_context(".clk(sys_clk ;"))


def test_port_connection_parser_success():
    node = PortConnectionParser.parse(get_context(".data_out(buffer_sig)"))
    assert isinstance(node, PortConnection)
    assert node.port_name == "data_out"


# ── ParameterOverrideParser ──────────────────────────────────────────

def test_parameter_override_parser_errors():
    with pytest.raises(RuntimeError, match=r"Expected '\.'"):
        ParameterOverrideParser.parse(get_context("WIDTH(32)"))

    with pytest.raises(RuntimeError, match="Expected parameter name"):
        ParameterOverrideParser.parse(get_context(". 123 (32)"))

    with pytest.raises(RuntimeError, match="Expected '\\('"):
        ParameterOverrideParser.parse(get_context(".WIDTH 32)"))

    with pytest.raises(RuntimeError, match="Expected '\\)'"):
        ParameterOverrideParser.parse(get_context(".WIDTH(32 ;"))


def test_parameter_override_parser_success():
    node = ParameterOverrideParser.parse(get_context(".DEPTH(SIZE * 2)"))
    assert isinstance(node, ParameterOverride)
    assert node.name == "DEPTH"
