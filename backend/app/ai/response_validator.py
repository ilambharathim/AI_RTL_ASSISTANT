"""
RIVA AI Response JSON Schema Validator.
Validates structural integrity and key constraints of LLM JSON outputs.
"""

from __future__ import annotations
import json
from typing import Dict, Any, Tuple


class ResponseValidator:
    """
    Validates structure and schema of LLM JSON responses.
    """

    def validate_schema(self, response_text: str) -> Tuple[bool, Dict[str, Any], str]:
        """
        Validates whether raw response is valid JSON matching RIVA AI explanation schema.
        """
        try:
            data = json.loads(response_text)
        except Exception as e:
            return False, {}, f"Invalid JSON string: {str(e)}"

        if not isinstance(data, dict):
            return False, {}, "Response root must be a JSON object"

        if "summary" not in data or "findings" not in data:
            return False, {}, "Missing required keys: 'summary' or 'findings'"

        if not isinstance(data.get("findings"), list):
            return False, {}, "'findings' must be a list"

        return True, data, "Schema validation successful"
