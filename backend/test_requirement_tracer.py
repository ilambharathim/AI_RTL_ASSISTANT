"""
Unit tests for RequirementTracer.
"""

from app.domain.requirement import Requirement
from app.analysis.traceability.requirement_tracer import RequirementTracer
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer


def test_requirement_tracer_matching():
    code = """
    module fifo_ctrl(
        input logic clk,
        input logic reset,
        input logic [15:0] data_in,
        output logic [15:0] data_out
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

    req1 = Requirement(
        requirement_id="REQ-001",
        category="FUNCTIONAL",
        description="The data_out port shall output 16-bit data.",
        condition="data_out",
        expected_result="16-bit output",
    )

    req2 = Requirement(
        requirement_id="REQ-002",
        category="FUNCTIONAL",
        description="The status_flag signal shall indicate overflow.",
        condition="status_flag",
        expected_result="1-bit flag",
    )

    tracer = RequirementTracer()
    trace_result = tracer.trace([req1, req2], semantic_model)

    links = trace_result["links"]
    diagnostics = trace_result["diagnostics"]

    assert len(links) == 2
    req1_link = [l for l in links if l.requirement_id == "REQ-001"][0]
    assert req1_link.status == "PASSED"
    assert req1_link.target_signal == "data_out"

    req2_link = [l for l in links if l.requirement_id == "REQ-002"][0]
    assert req2_link.status == "FAILED"
    assert len(diagnostics) == 1
    assert diagnostics[0].code == "RIVA6002"
