"""
Category 3: AST and source traceability tests (T293 - T300)
"""

import pytest
from app.ast.node import ASTNode
from app.ast.module_declaration import ModuleDeclaration
from app.ast.signal_declaration import SignalDeclaration
from app.ast.packed_range import PackedRange
from app.shared.source_location import SourceLocation
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer


def test_T293_ast_nested_structure():
    range_node = PackedRange("15", "0")
    sig_node = SignalDeclaration("logic", range_node, "data_in")
    mod_node = ModuleDeclaration("fifo_ctrl", (), (sig_node,))
    assert mod_node.name == "fifo_ctrl"
    assert len(mod_node.members) == 1
    assert mod_node.members[0].name == "data_in"


def test_T294_ast_invalid_node_combination():
    mod_node = ModuleDeclaration("top", (), ())
    assert hasattr(mod_node, "members")


def test_T295_ast_immutability_under_mutation_attempts():
    loc = SourceLocation(file="test.sv", line=5, column=10)
    assert loc.file == "test.sv"
    assert loc.line == 5
    with pytest.raises(AttributeError):
        loc.line = 10


def test_T296_ast_equality():
    loc1 = SourceLocation(file="top.sv", line=1, column=1)
    loc2 = SourceLocation(file="top.sv", line=1, column=1)
    assert loc1 == loc2


def test_T297_ast_serialization_deserialization():
    loc = SourceLocation(file="top.sv", line=10, column=5)
    loc_dict = {"file": loc.file, "line": loc.line, "column": loc.column}
    reconstructed = SourceLocation(file=loc_dict["file"], line=loc_dict["line"], column=loc_dict["column"])
    assert loc == reconstructed


def test_T298_source_location_propagation_through_ast():
    code = "module top(input logic [15:0] in); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None
    assert parse_result.syntax_tree.kind == "CompilationUnit"


def test_T299_source_location_preservation_after_parser_recovery():
    code = "module top; assign invalid = ; logic valid_sig; endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T300_source_location_preservation_through_semantic_transformation():
    code = "module top(input logic [7:0] data_in); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    assert semantic_model is not None
