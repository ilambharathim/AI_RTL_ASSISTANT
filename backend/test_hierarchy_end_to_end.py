"""
End-to-end tests for design hierarchy elaboration and module instantiations.
"""

from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.elaboration.elaborator import Elaborator
from app.elaboration.hierarchy_builder import HierarchyTreeBuilder


def test_end_to_end_hierarchy_elaboration():
    code = """
    module child(
        input logic a,
        output logic y
    );
        assign y = a;
    endmodule

    module top(
        input logic in_sig,
        output logic out_sig
    );
        child u_child (
            .a(in_sig),
            .y(out_sig)
        );
    endmodule
    """

    lexer = RTLLexer()
    tokens = lexer.tokenize(code)

    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful
    syntax_tree = parse_result.syntax_tree

    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(syntax_tree)

    elaborator = Elaborator()
    elaborated_model = elaborator.elaborate(syntax_tree, semantic_model)

    tree_builder = HierarchyTreeBuilder()
    hierarchy_trees = tree_builder.build_tree(syntax_tree)

    assert len(hierarchy_trees) == 1
    top_node = hierarchy_trees[0]
    assert top_node.name == "top"
    assert top_node.module_name == "top"
    assert len(top_node.children) == 1

    child_node = top_node.children[0]
    assert child_node.name == "u_child"
    assert child_node.module_name == "child"
    assert len(child_node.children) == 0


def test_parameterized_hierarchy_elaboration():
    code = """
    module adder #(
        parameter WIDTH = 8
    )(
        input logic [WIDTH-1:0] a,
        input logic [WIDTH-1:0] b,
        output logic [WIDTH-1:0] sum
    );
        assign sum = a + b;
    endmodule

    module top_adder();
        logic [15:0] x, y, z;

        adder #(
            .WIDTH(16)
        ) u_add16 (
            .a(x),
            .b(y),
            .sum(z)
        );
    endmodule
    """

    lexer = RTLLexer()
    tokens = lexer.tokenize(code)

    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful
    syntax_tree = parse_result.syntax_tree

    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(syntax_tree)

    elaborator = Elaborator()
    elaborated_model = elaborator.elaborate(syntax_tree, semantic_model)

    tree_builder = HierarchyTreeBuilder()
    hierarchy_trees = tree_builder.build_tree(syntax_tree)

    assert len(hierarchy_trees) == 1
    top_node = hierarchy_trees[0]
    assert top_node.name == "top_adder"
    assert len(top_node.children) == 1
    assert top_node.children[0].name == "u_add16"
    assert top_node.children[0].module_name == "adder"
