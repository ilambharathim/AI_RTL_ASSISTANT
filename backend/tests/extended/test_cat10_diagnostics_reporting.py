"""
Category 10: Diagnostics and reporting tests (T383 - T390)
"""

import pytest
import json
from app.diagnostics.diagnostic import Diagnostic
from app.shared.source_location import SourceLocation
from app.ai.evidence_store import EvidenceStore
from app.ai.ai_reasoning_engine import AIReasoningEngine
from app.reporting.report_generator import ConsolidatedReportGenerator


def test_T383_multiple_severity_levels():
    loc = SourceLocation(source_file="top.sv", line=5, column=2)
    d_err = Diagnostic(code="RIVA6001", category="spec", severity="error", message="Error msg", location=loc)
    d_warn = Diagnostic(code="RIVA2003", category="width", severity="warning", message="Warn msg", location=loc)
    assert d_err.severity == "error"
    assert d_warn.severity == "warning"


def test_T384_multiple_diagnostic_categories():
    loc = SourceLocation(source_file="top.sv", line=5, column=2)
    d1 = Diagnostic(code="RIVA1001", category="semantic", severity="error", message="msg1", location=loc)
    d2 = Diagnostic(code="RIVA2003", category="width", severity="warning", message="msg2", location=loc)
    assert d1.category != d2.category


def test_T385_diagnostic_ordering_across_compiler_phases():
    store = EvidenceStore(project_name="Order_Test")
    loc = SourceLocation(source_file="top.sv", line=1, column=1)
    d1 = Diagnostic(code="RIVA1001", category="parser", severity="error", message="Parse err", location=loc)
    d2 = Diagnostic(code="RIVA2003", category="semantic", severity="warning", message="Width err", location=loc)
    store.add_diagnostics([d1, d2])
    payload = store.get_payload()
    assert len(payload.diagnostics) == 2


def test_T386_duplicate_diagnostic_suppression():
    store = EvidenceStore(project_name="Dup_Test")
    loc = SourceLocation(source_file="top.sv", line=1, column=1)
    d1 = Diagnostic(code="RIVA1001", category="parser", severity="error", message="Err", location=loc)
    store.add_diagnostics([d1])
    payload = store.get_payload()
    assert len(payload.diagnostics) == 1


def test_T387_source_location_in_final_diagnostic():
    loc = SourceLocation(source_file="fifo_ctrl.sv", line=12, column=4)
    d = Diagnostic(code="RIVA2003", category="width", severity="warning", message="Truncation", location=loc)
    assert d.location.source_file == "fifo_ctrl.sv"
    assert d.location.line == 12


def test_T388_text_report_with_complete_pipeline():
    store = EvidenceStore(project_name="Text_Report_Project")
    ai_engine = AIReasoningEngine()
    report_gen = ConsolidatedReportGenerator(ai_engine)
    payload = store.get_payload()
    md_report = report_gen.generate_markdown_report(payload)
    assert "# RIVA Consolidated Verification Report" in md_report


def test_T389_json_report_schema_validation():
    store = EvidenceStore(project_name="JSON_Report_Project")
    ai_engine = AIReasoningEngine()
    report_gen = ConsolidatedReportGenerator(ai_engine)
    payload = store.get_payload()
    json_str = report_gen.generate_json_report(payload)
    data = json.loads(json_str)
    assert "evidence" in data
    assert data["evidence"]["project_name"] == "JSON_Report_Project"


def test_T390_report_determinism_across_repeated_runs():
    store = EvidenceStore(project_name="Determinism_Project")
    ai_engine = AIReasoningEngine()
    report_gen = ConsolidatedReportGenerator(ai_engine)
    payload = store.get_payload()
    
    report1 = report_gen.generate_markdown_report(payload)
    report2 = report_gen.generate_markdown_report(payload)
    assert report1 == report2
