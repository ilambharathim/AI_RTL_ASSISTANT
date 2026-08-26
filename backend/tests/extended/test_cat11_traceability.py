"""
Category 11: Requirement traceability tests (T391 - T396)
"""

import pytest
from app.domain.requirement import Requirement
from app.analysis.traceability.requirement_tracer import RequirementTracer, TraceabilityLink
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer


def test_T391_requirement_to_rtl_mapping():
    req = Requirement(requirement_id="REQ-01", category="FUNCTIONAL", description="data_out port shall output 16 bits", condition="data_out", expected_result="16 bits")
    code = "module top(output logic [15:0] data_out); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    tracer = RequirementTracer()
    result = tracer.trace([req], semantic_model)
    assert len(result["links"]) == 1
    assert result["links"][0].status == "PASSED"


def test_T392_rtl_to_requirement_mapping():
    req = Requirement(requirement_id="REQ-01", category="TIMING", description="reset sets empty flag HIGH", condition="empty", expected_result="1 bit")
    code = "module top(output logic empty); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    tracer = RequirementTracer()
    result = tracer.trace([req], semantic_model)
    assert result["links"][0].target_signal == "empty"


def test_T393_unmapped_requirement():
    req = Requirement(requirement_id="REQ-MISSING", category="FUNCTIONAL", description="nonexistent_sig shall exist", condition="nonexistent_sig", expected_result="8 bits")
    code = "module top(output logic [7:0] other_sig); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    tracer = RequirementTracer()
    result = tracer.trace([req], semantic_model)
    assert result["links"][0].status == "FAILED"


def test_T394_unmapped_rtl_construct():
    code = "module top(input logic extra_sig); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    tracer = RequirementTracer()
    result = tracer.trace([], semantic_model)
    assert len(result["links"]) == 0


def test_T395_multiple_rtl_elements_satisfying_one_requirement():
    req = Requirement(requirement_id="REQ-BUS", category="FUNCTIONAL", description="data bus port", condition="data", expected_result="8 bits")
    code = "module top(input logic [7:0] data); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    tracer = RequirementTracer()
    result = tracer.trace([req], semantic_model)
    assert result["links"][0].status == "PASSED"


def test_T396_traceability_preserved_through_pipeline():
    req = Requirement(requirement_id="REQ-TRACE", category="FUNCTIONAL", description="ctrl sig", condition="ctrl", expected_result="1 bit")
    code = "module top(output logic ctrl); endmodule"
    lexer = RTLLexer()
    tokens = lexer.tokenize(code)
    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(parse_result.syntax_tree)
    tracer = RequirementTracer()
    result = tracer.trace([req], semantic_model)
    assert len(result["links"]) == 1
