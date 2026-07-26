"""
Base contract for deterministic engineering validation rules.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import inspect
from typing import ClassVar

from app.domain.specification_ir import SpecificationIR
from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.rule_engine.validation_result import ValidationRuleResult


class ValidationRule(ABC):
    """
    Executes one deterministic validation rule against a SpecificationIR.
    """

    rule_id: ClassVar[str]
    description: ClassVar[str]
    stage: ClassVar[str] = "specification-validation"

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)

        if inspect.isabstract(cls):
            return

        rule_id = getattr(cls, "rule_id", None)
        description = getattr(cls, "description", None)
        stage = getattr(cls, "stage", None)

        if not isinstance(rule_id, str) or not rule_id.strip():
            raise TypeError(
                "concrete ValidationRule classes must define "
                "a non-empty string rule_id"
            )

        if not isinstance(description, str) or not description.strip():
            raise TypeError(
                "concrete ValidationRule classes must define "
                "a non-empty string description"
            )

        if not isinstance(stage, str) or not stage.strip():
            raise TypeError(
                "concrete ValidationRule classes must define "
                "a non-empty string stage"
            )

    def run(self, specification: SpecificationIR) -> ValidationRuleResult:
        """
        Validate input and output contracts around rule evaluation.
        """

        if not isinstance(specification, SpecificationIR):
            raise TypeError("specification must be a SpecificationIR")

        diagnostics = self._evaluate(specification)

        if type(diagnostics) is not tuple:
            raise TypeError(
                "validation rules must return a tuple of Diagnostic objects"
            )

        for diagnostic in diagnostics:
            if not isinstance(diagnostic, Diagnostic):
                raise TypeError(
                    "validation rules must return only Diagnostic objects"
                )

            if diagnostic.stage != self.stage:
                raise ValueError(
                    "validation rule diagnostics must use the rule stage"
                )

        return ValidationRuleResult(
            rule_id=self.rule_id,
            diagnostics=diagnostics,
        )

    @abstractmethod
    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        """
        Return deterministic diagnostics without mutating specification.
        """
