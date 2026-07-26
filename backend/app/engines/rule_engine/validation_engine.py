"""
Deterministic ordered execution engine for specification validation rules.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.domain.specification_ir import SpecificationIR
from app.engines.rule_engine.validation_engine_result import (
    ValidationEngineResult,
)
from app.engines.rule_engine.validation_rule import ValidationRule


class ValidationEngine:
    """
    Executes registered validation rules in deterministic declaration order.
    """

    def __init__(self, rules: Sequence[ValidationRule]) -> None:
        if isinstance(rules, (str, bytes)) or not isinstance(rules, Sequence):
            raise TypeError("rules must be a sequence of ValidationRule objects")

        validated_rules: list[ValidationRule] = []
        seen_rule_ids: set[str] = set()

        for rule in rules:
            if not isinstance(rule, ValidationRule):
                raise TypeError(
                    "rules must contain only ValidationRule objects"
                )

            if rule.rule_id in seen_rule_ids:
                raise ValueError(
                    f"duplicate validation rule_id: {rule.rule_id}"
                )

            seen_rule_ids.add(rule.rule_id)
            validated_rules.append(rule)

        self._rules = tuple(validated_rules)

    @property
    def rules(self) -> tuple[ValidationRule, ...]:
        return self._rules

    def run(self, specification: SpecificationIR) -> ValidationEngineResult:
        """
        Execute every rule once and preserve registration order.
        """

        if not isinstance(specification, SpecificationIR):
            raise TypeError("specification must be a SpecificationIR")

        return ValidationEngineResult(
            rule_results=tuple(
                rule.run(specification)
                for rule in self._rules
            )
        )
