"""
Deterministic end-to-end specification analysis pipeline.
"""

from collections.abc import Sequence
from pathlib import Path

from app.engines.rule_engine.specification_validation_rules import (
    default_specification_validation_rules,
)
from app.engines.rule_engine.validation_engine import ValidationEngine
from app.engines.rule_engine.validation_rule import ValidationRule
from app.parsers.specification.lexer import SpecificationLexer
from app.parsers.specification.normalizer import DocumentNormalizer
from app.parsers.specification.parser import SpecificationParser
from app.parsers.specification.pipeline_result import (
    SpecificationPipelineResult,
)
from app.parsers.specification.reader import SpecificationReader
from app.parsers.specification.semantic_builder import (
    SpecificationSemanticBuilder,
)


class SpecificationPipeline:
    """
    Execute the complete deterministic specification frontend.

    Validation runs against the exact SpecificationIR instance produced by
    the semantic builder. Fresh phase results are created for every call.
    """

    def __init__(
        self,
        rules: Sequence[ValidationRule] | None = None,
    ) -> None:
        selected_rules = (
            default_specification_validation_rules()
            if rules is None
            else rules
        )

        self._validation_engine = ValidationEngine(selected_rules)

    @property
    def rules(self) -> tuple[ValidationRule, ...]:
        return self._validation_engine.rules

    def run(
        self,
        source: str | Path,
    ) -> SpecificationPipelineResult:
        source_path = Path(source)

        text = SpecificationReader.read(source_path)
        normalized_text = DocumentNormalizer.normalize(text)

        tokens = SpecificationLexer(
            normalized_text,
            source_file=str(source_path),
        ).tokenize()

        parse_result = SpecificationParser(
            tokens
        ).parse_with_diagnostics()

        semantic_result = SpecificationSemanticBuilder(
            parse_result.document
        ).build()

        validation_result = self._validation_engine.run(
            semantic_result.specification
        )

        return SpecificationPipelineResult(
            parse_result=parse_result,
            semantic_result=semantic_result,
            validation_result=validation_result,
        )
