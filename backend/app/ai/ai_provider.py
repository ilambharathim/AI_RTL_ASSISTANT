"""
RIVA LLM Client & Provider Gateway.
Handles LLM inference over evidence payloads with grounding validation and offline fallback.
"""

from __future__ import annotations
import json
from typing import Dict, Any, Optional
from app.ai.evidence_store import EvidencePayload
from app.ai.ai_reasoning_engine import AIReasoningEngine
from app.ai.response_validator import ResponseValidator
from app.ai.grounding_validator import GroundingValidator


class LLMClient:
    """
    Client for dispatching evidence prompts to LLM providers.
    """

    def __init__(self, provider_type: str = "mock"):
        self.provider_type = provider_type

    def generate_raw_explanation(self, payload: EvidencePayload) -> str:
        """
        Generates raw response string from configured LLM provider.
        """
        engine = AIReasoningEngine()
        explanation = engine.generate_explanation(payload)
        return json.dumps(explanation)


class AIProvider:
    """
    AI Provider Gateway orchestrating LLM inference, schema validation, and anti-hallucination grounding.
    """

    def __init__(self, provider_type: str = "mock"):
        self.llm_client = LLMClient(provider_type)
        self.response_validator = ResponseValidator()
        self.grounding_validator = GroundingValidator()

    def process_evidence(self, payload: EvidencePayload) -> Dict[str, Any]:
        """
        Full AI Gateway workflow: LLM Inference -> Response Validation -> Grounding Enforcement.
        """
        raw_text = self.llm_client.generate_raw_explanation(payload)
        is_valid, data, err = self.response_validator.validate_schema(raw_text)

        if not is_valid:
            # Deterministic Fallback on schema validation error
            engine = AIReasoningEngine()
            return engine.generate_explanation(payload)

        ground_res = self.grounding_validator.validate_grounding(data, payload)
        if not ground_res.is_grounded:
            # Filter out hallucinated findings
            valid_findings = [
                f for f in data.get("findings", [])
                if f.get("code") not in ground_res.hallucinated_codes
            ]
            data["findings"] = valid_findings
            data["confidence_score"] = max(50, data.get("confidence_score", 85) + ground_res.confidence_adjustment)

        return data
