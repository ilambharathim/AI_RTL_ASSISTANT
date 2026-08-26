"""
Tests for Control Flow Graph (CFG) and Dataflow analysis integration with diagnostics.
"""

from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.analysis.cfg.cfg_builder import CFGBuilder
from app.analysis.dataflow.runtime.dataflow_runner import DataFlowRunner
from app.analysis.dataflow.analyses.live_variables import LiveVariableAnalysis
from app.diagnostics.diagnostic_engine import DiagnosticEngine


def test_cfg_builder_and_live_variables():
    code = """
    module cfg_demo(
        input logic sel,
        input logic [7:0] a,
        input logic [7:0] b,
        output logic [7:0] y
    );
        always_comb begin
            if (sel) begin
                y = a;
            end else begin
                y = b;
            end
        end
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

    cfg_builder = CFGBuilder()
    cfg = cfg_builder.build(syntax_tree)

    assert cfg is not None
    assert len(cfg.blocks) >= 3

    from app.analysis.dataflow.worklist_solver import WorklistSolver
    solver = WorklistSolver()
    df_result = solver.solve(cfg, LiveVariableAnalysis())
    assert df_result is not None

    diagnostic_engine = DiagnosticEngine()
    diagnostics = diagnostic_engine.analyze(semantic_model)

    assert isinstance(diagnostics, list)
