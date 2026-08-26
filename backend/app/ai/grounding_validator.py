"""
RIVA AI Grounding & Anti-Hallucination Validator.
Verifies that AI reasoning explanations strictly reference facts present in the EvidencePayload.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List
from app.ai.evidence_store import EvidencePayload


@dataclass(slots=True)
class GroundingValidationResult:
    """
    Result of AI grounding validation.
    """
    is_grounded: bool
    hallucinated_codes: List[str]
    hallucinated_signals: List[str]
    confidence_adjustment: int


class GroundingValidator:
    """
    Enforces strict evidence grounding for AI-generated explanations.
    """

    def validate_grounding(
        self,
        explanation: Dict[str, Any],
        payload: EvidencePayload,
    ) -> GroundingValidationResult:
        """
        Validates that AI output contains zero hallucinated diagnostic codes or signal names.
        """
        emitted_codes = {d.code for d in payload.diagnostics}
        emitted_signals = {t.target_signal for t in payload.traceability_links}

        hallucinated_codes: List[str] = []
        hallucinated_signals: List[str] = []

        findings = explanation.get("findings", [])
        for f in findings:
            code = f.get("code", "")
            if code and code not in emitted_codes:
                hallucinated_codes.append(code)

            signal = f.get("signal", "")
            if signal and emitted_signals and signal not in emitted_signals:
                hallucinated_signals.append(signal)

        is_grounded = len(hallucinated_codes) == 0 and len(hallucinated_signals) == 0
        confidence_adj = 0 if is_grounded else -30

        return GroundingValidationResult(
            is_grounded=is_grounded,
            hallucinated_codes=hallucinated_codes,
            hallucinated_signals=hallucinated_signals,
            confidence_adjustment=confidence_adj,
        )
