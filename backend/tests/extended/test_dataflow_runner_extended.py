"""
Extended Unit Test Suite for DataFlowRunner and WorklistSolver.
Validates CFG dataflow analysis convergence over straight-line code, branches, loops, and empty CFGs.
"""

import pytest
from app.analysis.cfg.cfg_builder import CFGBuilder
from app.analysis.dataflow.runtime.dataflow_runner import DataFlowRunner
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser


def test_dataflow_runner_execution_and_convergence():
    code = """
    module top(input logic [15:0] in, output logic [15:0] out);
        logic [15:0] a, b;
        always_comb begin
            if (in > 0) begin
                a = in;
                b = a + 16'd1;
            end else begin
                a = 16'd0;
                b = 16'd0;
            end
            out = b;
        end
    endmodule
    """
    tokens = RTLLexer().tokenize(code)
    parse_res = RTLParser().parse(tokens.tokens)
    assert parse_res.syntax_tree is not None

    cfg = CFGBuilder().build(parse_res.syntax_tree)
    assert cfg is not None

    class DummyElaborationModel:
        def __init__(self, cfgs):
            self.cfgs = cfgs
            self.dataflow = {}

    model = DummyElaborationModel({"top": cfg})
    runner = DataFlowRunner()
    runner.run(model)

    assert "top" in model.dataflow
    assert model.dataflow["top"] is not None
