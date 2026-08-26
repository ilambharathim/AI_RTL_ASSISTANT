"""
Consolidated Verification Report Generator.
Generates comprehensive Markdown and JSON verification reports from evidence payloads and AI reasoning.
"""

from __future__ import annotations
import json
from typing import Dict, Any

from app.ai.evidence_store import EvidencePayload
from app.ai.ai_reasoning_engine import AIReasoningEngine


class ConsolidatedReportGenerator:
    """
    Generates consolidated engineering verification reports.
    """

    def __init__(self, reasoning_engine: AIReasoningEngine | None = None):
        self.reasoning_engine = reasoning_engine or AIReasoningEngine()

    def generate_json_report(self, payload: EvidencePayload) -> str:
        """
        Returns complete json-formatted verification report.
        """
        ai_findings = self.reasoning_engine.generate_explanation(payload)
        report_data = {
            "evidence": payload.to_dict(),
            "ai_reasoning": ai_findings,
        }
        return json.dumps(report_data, indent=2)

    def generate_markdown_report(self, payload: EvidencePayload) -> str:
        """
        Returns human-readable Markdown engineering report.
        """
        data = payload.to_dict()
        ai_findings = self.reasoning_engine.generate_explanation(payload)

        status_flag = "PASSED" if data["errors_count"] == 0 else "FAILED"

        report = f"""# RIVA Consolidated Verification Report

**Project**: {payload.project_name}  
**Verification Status**: `{status_flag}`  
**Overall Confidence**: {ai_findings['confidence_score']}%  

---

## Executive Summary
{ai_findings['summary']}

---

## Diagnostic Findings Overview
- **Errors**: {data['errors_count']}
- **Warnings**: {data['warnings_count']}
- **Total Diagnostics**: {data['total_diagnostics']}

### Detailed Diagnostics Table
| Code | Category | Severity | Location | Message | Suggestion |
|------|----------|----------|----------|---------|------------|
"""
        for d in data["diagnostics"]:
            report += f"| `{d['code']}` | {d['category']} | {d['severity']} | `{d['location']}` | {d['message']} | {d['suggestion']} |\n"

        if not data["diagnostics"]:
            report += "*No diagnostic violations detected.*\n"

        report += """
---

## Specification Traceability
| Requirement ID | Target Signal | Status | Details |
|----------------|---------------|--------|---------|
"""
        for t in data["traceability"]:
            report += f"| `{t['req_id']}` | `{t['signal']}` | `{t['status']}` | {t['details']} |\n"

        if not data["traceability"]:
            report += "*No specification traceability links evaluated.*\n"

        report += """
---

## AI Grounded Explanations & Recommended Fixes
"""
        for f in ai_findings["findings"]:
            report += f"### [{f['code']}] at `{f['location']}`\n"
            report += f"**Explanation**: {f['explanation']}\n\n"
            report += f"**Recommended Fix**: `{f['suggested_fix']}`\n\n"

        report += "---\n*Generated automatically by RIVA Verification Platform.*"
        return report
