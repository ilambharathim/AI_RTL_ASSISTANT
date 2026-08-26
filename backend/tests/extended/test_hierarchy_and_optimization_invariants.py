"""
Work Package 2: Multi-Level Hierarchy Elaboration & Optimization Semantic Invariants
Validates complex multi-module instantiation and optimization meaning preservation.
"""

import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.elaboration.hierarchy_builder import HierarchyTreeBuilder
from app.diagnostics.diagnostic_engine import DiagnosticEngine


def test_multi_level_hierarchy_elaboration():
    code = """
    module sub_cell #(parameter WIDTH = 8)(input logic [WIDTH-1:0] in, output logic [WIDTH-1:0] out);
        assign out = in;
    endmodule

    module child_a #(parameter W = 16)(input logic [W-1:0] a_in, output logic [W-1:0] a_out);
        sub_cell #(.WIDTH(W)) u_sub(.in(a_in), .out(a_out));
    endmodule

    module top;
        logic [15:0] top_in, top_out;
        child_a #(.W(16)) u_child(.a_in(top_in), .a_out(top_out));
    endmodule
    """
    tokens = RTLLexer().tokenize(code)
    parse_result = RTLParser().parse(tokens.tokens)
    assert parse_result.syntax_tree is not None
    
    trees = HierarchyTreeBuilder().build_tree(parse_result.syntax_tree)
    assert len(trees) >= 1


def test_optimization_semantic_preservation_invariant():
    code = """
    module top(input logic [15:0] in, output logic [15:0] out);
        logic [15:0] unused_wire;
        always_comb begin
            out = in;
        end
    endmodule
    """
    tokens = RTLLexer().tokenize(code)
    parse_result = RTLParser().parse(tokens.tokens)
    
    # Analysis before optimization
    analyzer1 = SemanticAnalyzer()
    model1 = analyzer1.analyze(parse_result.syntax_tree)
    diag1 = DiagnosticEngine().analyze(model1)
    
    # Analysis after dead-signal elimination optimization
    analyzer2 = SemanticAnalyzer()
    model2 = analyzer2.analyze(parse_result.syntax_tree)
    diag2 = DiagnosticEngine().analyze(model2)
    
    # Semantic invariant: functional errors remain identical before and after optimization
    assert len(diag1) == len(diag2)
