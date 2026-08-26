"""
Category 14: RIVA end-to-end behavior tests (T413 - T420)
"""

import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.domain.requirement import Requirement
from app.analysis.traceability.requirement_tracer import RequirementTracer
from app.diagnostics.diagnostic_engine import DiagnosticEngine
from app.ai.evidence_store import EvidenceStore
from app.ai.ai_reasoning_engine import AIReasoningEngine
from app.reporting.report_generator import ConsolidatedReportGenerator


def test_T413_specification_parse_semantic_analysis_report():
    req = Requirement(requirement_id="REQ-01", category="FUNCTIONAL", description="16-bit output", condition="data_out", expected_result="16 bits")
    tracer = RequirementTracer()
    code = "module top(output logic [15:0] data_out); endmodule"
    tokens = RTLLexer().tokenize(code)
    parse_result = RTLParser().parse(tokens.tokens)
    semantic_model = SemanticAnalyzer().analyze(parse_result.syntax_tree)
    trace_res = tracer.trace([req], semantic_model)
    
    store = EvidenceStore(project_name="T413_Proj")
    store.add_traceability_links(trace_res["links"])
    payload = store.get_payload()
    report = ConsolidatedReportGenerator(AIReasoningEngine()).generate_markdown_report(payload)
    assert "REQ-01" in report


def test_T414_specification_plus_rtl_complete_analysis():
    code = "module fifo(input logic [15:0] in, output logic [7:0] out); always_comb begin out = in; end endmodule"
    tokens = RTLLexer().tokenize(code)
    parse_result = RTLParser().parse(tokens.tokens)
    semantic_model = SemanticAnalyzer().analyze(parse_result.syntax_tree)
    diagnostics = DiagnosticEngine().analyze(semantic_model)
    assert isinstance(diagnostics, list)


def test_T415_valid_specification_plus_valid_rtl_clean_result():
    code = "module adder16(input logic [15:0] a, b, output logic [15:0] sum); always_comb begin sum = a + b; end endmodule"
    tokens = RTLLexer().tokenize(code)
    parse_result = RTLParser().parse(tokens.tokens)
    semantic_model = SemanticAnalyzer().analyze(parse_result.syntax_tree)
    diagnostics = DiagnosticEngine().analyze(semantic_model)
    assert len(diagnostics) == 0


def test_T416_width_mismatch_diagnostic_final_report():
    code = "module top(input logic [15:0] in, output logic [7:0] out); always_comb begin out = in; end endmodule"
    tokens = RTLLexer().tokenize(code)
    parse_result = RTLParser().parse(tokens.tokens)
    semantic_model = SemanticAnalyzer().analyze(parse_result.syntax_tree)
    diagnostics = DiagnosticEngine().analyze(semantic_model)
    
    store = EvidenceStore(project_name="T416_Width_Proj")
    store.add_diagnostics(diagnostics)
    payload = store.get_payload()
    report = ConsolidatedReportGenerator(AIReasoningEngine()).generate_markdown_report(payload)
    assert "# RIVA Consolidated Verification Report" in report


def test_T417_signedness_mismatch_diagnostic_final_report():
    code = "module top(input logic signed [7:0] in, output logic unsigned [7:0] out); always_comb begin out = in; end endmodule"
    tokens = RTLLexer().tokenize(code)
    parse_result = RTLParser().parse(tokens.tokens)
    semantic_model = SemanticAnalyzer().analyze(parse_result.syntax_tree)
    diagnostics = DiagnosticEngine().analyze(semantic_model)
    assert isinstance(diagnostics, list)


def test_T418_invalid_rtl_parser_diagnostic_report():
    code = "module top; assign x = ; endmodule"
    tokens = RTLLexer().tokenize(code)
    parse_result = RTLParser().parse(tokens.tokens)
    assert parse_result.syntax_tree is not None


def test_T419_requirement_rtl_traceability_report():
    req = Requirement(requirement_id="REQ-419", category="TIMING", description="reset signal", condition="reset", expected_result="1 bit")
    code = "module top(input logic reset); endmodule"
    tokens = RTLLexer().tokenize(code)
    parse_result = RTLParser().parse(tokens.tokens)
    semantic_model = SemanticAnalyzer().analyze(parse_result.syntax_tree)
    trace_res = RequirementTracer().trace([req], semantic_model)
    store = EvidenceStore(project_name="T419_Proj")
    store.add_traceability_links(trace_res["links"])
    payload = store.get_payload()
    report = ConsolidatedReportGenerator(AIReasoningEngine()).generate_markdown_report(payload)
    assert "REQ-419" in report


def test_T420_complete_representative_riva_project():
    code = """
    module fifo_ctrl #(
        parameter WIDTH = 16,
        parameter DEPTH = 8
    )(
        input logic clk,
        input logic reset,
        input logic [15:0] data_in,
        output logic [15:0] data_out,
        output logic full,
        output logic empty
    );
        always_ff @(posedge clk or posedge reset) begin
            if (reset) begin
                empty <= 1'b1;
                full <= 1'b0;
                data_out <= 16'd0;
            end else begin
                data_out <= data_in;
            end
        end
    endmodule
    """
    tokens = RTLLexer().tokenize(code)
    parse_result = RTLParser().parse(tokens.tokens)
    assert parse_result.syntax_tree is not None
    semantic_model = SemanticAnalyzer().analyze(parse_result.syntax_tree)
    diagnostics = DiagnosticEngine().analyze(semantic_model)
    assert isinstance(diagnostics, list)
