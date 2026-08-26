"""
AI Reasoning Engine.
Grounded AI interpretation layer sitting directly above deterministic evidence payload.
"""

from __future__ import annotations
from typing import Dict, List, Any
from app.ai.evidence_store import EvidencePayload


class AIReasoningEngine:
    """
    Constructs knowledge-grounded explanations and repair recommendations based strictly on evidence payload.
    """

    def generate_explanation(self, payload: EvidencePayload) -> Dict[str, Any]:
        """
        Synthesizes deterministic evidence into human-readable engineering explanations.
        """
        data = payload.to_dict()
        explanations: List[Dict[str, str]] = []

        for diag in data["diagnostics"]:
            code = diag["code"]
            msg = diag["message"]
            loc = diag["location"]
            sug = diag["suggestion"]

            explanation_text = (
                f"Diagnostic [{code}] identified in location '{loc}': {msg}. "
                f"Deterministic evidence shows this issue requires: {sug}"
            )

            explanations.append(
                {
                    "code": code,
                    "location": loc,
                    "explanation": explanation_text,
                    "suggested_fix": sug,
                }
            )

        spec_mismatches = [t for t in data["traceability"] if t["status"] == "FAILED"]
        for spec in spec_mismatches:
            explanations.append(
                {
                    "code": "SPEC_MISMATCH",
                    "location": "<specification>",
                    "explanation": f"Specification requirement {spec['req_id']} failed verification: {spec['details']}",
                    "suggested_fix": f"Align signal '{spec['signal']}' implementation with specification requirement {spec['req_id']}.",
                }
            )

        summary_text = (
            f"RIVA deterministic verification engine completed analysis for '{payload.project_name}'. "
            f"Found {data['errors_count']} errors and {data['warnings_count']} warnings across "
            f"{len(data['diagnostics'])} deterministic diagnostic rules. "
            f"Specification traceability verified {len(data['traceability'])} requirement links."
        )

        return {
            "summary": summary_text,
            "findings": explanations,
            "confidence_score": 95 if data["errors_count"] == 0 else 85,
        }

    def format_llm_prompt(self, payload: EvidencePayload) -> str:
        """
        Formats evidence payload into a strict prompt template for LLM integration.
        """
        data = payload.to_dict()
        prompt = (
            f"SYSTEM: You are RIVA (RTL Intelligent Verification Assistant).\n"
            f"Use the following deterministic evidence to explain findings for project '{data['project_name']}':\n\n"
            f"EVIDENCE PAYLOAD:\n"
            f"- Diagnostics: {data['diagnostics']}\n"
            f"- Traceability Links: {data['traceability']}\n"
            f"- Simulation Results: {data['simulation']}\n"
            f"- Waveform Observations: {data['waveform']}\n\n"
            f"USER QUERY: Explain the root cause of verification failures and provide RTL repair recommendations."
        )
        return prompt
