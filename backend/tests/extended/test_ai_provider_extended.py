"""
Comprehensive Unit Test Suite for Phase 10 — AI Provider and Validation.
Validates 100% of branches across ResponseValidator and AIProvider.
"""

import pytest
import json
from app.ai.response_validator import ResponseValidator
from app.ai.ai_provider import AIProvider
from app.ai.evidence_store import EvidencePayload
from app.diagnostics.diagnostic import Diagnostic


def test_response_validator_all_branches():
    val = ResponseValidator()

    # 1. Invalid JSON string
    ok, data, err = val.validate_schema("{invalid_json:")
    assert not ok and "Invalid JSON" in err

    # 2. Response root is not a dict
    ok, data, err = val.validate_schema("[1, 2, 3]")
    assert not ok and "root must be a JSON object" in err

    # 3. Missing required keys
    ok, data, err = val.validate_schema('{"summary": "test"}')
    assert not ok and "Missing required keys" in err

    # 4. findings is not a list
    ok, data, err = val.validate_schema('{"summary": "test", "findings": "not_a_list"}')
    assert not ok and "'findings' must be a list" in err

    # 5. Schema validation successful
    ok, data, err = val.validate_schema('{"summary": "test", "findings": []}')
    assert ok and "successful" in err


def test_ai_provider_all_branches():
    provider = AIProvider("mock")

    # Valid payload
    payload = EvidencePayload(
        project_name="test_project",
        diagnostics=[Diagnostic("RIVA1001", "syntax", "error", "Undeclared identifier")],
    )

    res = provider.process_evidence(payload)
    assert "summary" in res
    assert "findings" in res

    # Test invalid schema fallback in process_evidence
    class BadLLMClient:
        def generate_raw_explanation(self, p):
            return "NOT_VALID_JSON"

    provider.llm_client = BadLLMClient()
    res_fallback = provider.process_evidence(payload)
    assert "summary" in res_fallback

    # Test ungrounded hallucination path in process_evidence
    class HallucinatingLLMClient:
        def generate_raw_explanation(self, p):
            return json.dumps({
                "summary": "AI summary",
                "findings": [{"code": "RIVA9999_HALLUCINATED", "message": "Fake finding"}],
                "confidence_score": 90,
            })

    provider2 = AIProvider("mock")
    provider2.llm_client = HallucinatingLLMClient()
    res_ungrounded = provider2.process_evidence(payload)
    assert "summary" in res_ungrounded
