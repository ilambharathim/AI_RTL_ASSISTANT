"""
End-to-end regression for the validated specification pipeline.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from app.domain.specification_ir import SpecificationIR
from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.engines.rule_engine.validation_rule import ValidationRule
from app.parsers.specification.pipeline import SpecificationPipeline


_VALID_SPECIFICATION = """Project Title: 2-to-1 Multiplexer

Module Name:
mux2to1

Description:
Design a combinational 2-to-1 multiplexer.

Inputs:
- a : 1-bit input
- b : 1-bit input
- sel : 1-bit select signal

Output:
- y : 1-bit output

Functional Requirements:
1. If sel = 0, output y shall be equal to input a.
2. If sel = 1, output y shall be equal to input b.

Timing:
Pure combinational logic.

Language:
SystemVerilog
"""


class _RecordingRule(ValidationRule):
    rule_id = "TEST-PIPELINE-RULE-001"
    description = "Record the validated SpecificationIR identity."

    def __init__(self) -> None:
        self.observed_specifications: list[SpecificationIR] = []

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        self.observed_specifications.append(specification)
        return ()


def _write_specification(
    directory: str,
    name: str,
    content: str,
) -> Path:
    source_path = Path(directory) / name
    source_path.write_text(content, encoding="utf-8")
    return source_path


def test_valid_pipeline_result_maps_and_validates_specification() -> None:
    with TemporaryDirectory() as directory:
        source_path = _write_specification(
            directory,
            "mux_specification.txt",
            _VALID_SPECIFICATION,
        )

        result = SpecificationPipeline().run(source_path)

        assert result.is_successful
        assert result.diagnostics == ()
        assert result.diagnostic_count == 0
        assert result.parse_result.is_successful
        assert result.semantic_result.is_successful
        assert result.validation_result.is_successful
        assert result.validation_result.executed_rule_count == 9

        specification = result.specification

        assert specification.metadata.project_name == "2-to-1 Multiplexer"
        assert specification.metadata.module_name == "mux2to1"
        assert specification.metadata.language == "SystemVerilog"
        assert specification.metadata.source_file == str(source_path)
        assert [port.name for port in specification.ports] == [
            "a",
            "b",
            "sel",
            "y",
        ]
        assert [
            requirement.requirement_id
            for requirement in specification.requirements
        ] == [
            "REQ_001",
            "REQ_002",
        ]


def test_pipeline_aggregates_diagnostics_in_phase_order() -> None:
    with TemporaryDirectory() as directory:
        source_path = _write_specification(
            directory,
            "empty_specification.txt",
            "",
        )

        result = SpecificationPipeline().run(source_path)

        assert [diagnostic.code for diagnostic in result.diagnostics] == [
            "SPEC-SEM-012",
            "SPEC-VAL-001",
            "SPEC-VAL-002",
            "SPEC-VAL-003",
            "SPEC-VAL-004",
        ]
        assert [
            diagnostic.stage for diagnostic in result.diagnostics
        ] == [
            "specification-semantic-builder",
            "specification-validation",
            "specification-validation",
            "specification-validation",
            "specification-validation",
        ]
        assert result.error_count == 3
        assert result.warning_count == 2
        assert result.info_count == 0
        assert result.has_errors
        assert not result.is_successful
        assert all(
            diagnostic.source_file == str(source_path)
            for diagnostic in result.diagnostics
        )


def test_validation_receives_semantic_builder_specification() -> None:
    with TemporaryDirectory() as directory:
        source_path = _write_specification(
            directory,
            "identity_specification.txt",
            _VALID_SPECIFICATION,
        )

        recording_rule = _RecordingRule()
        result = SpecificationPipeline(
            rules=(recording_rule,),
        ).run(source_path)

        assert recording_rule.observed_specifications == [
            result.specification
        ]
        assert (
            recording_rule.observed_specifications[0]
            is result.specification
        )


def test_repeated_pipeline_runs_are_deterministic_and_independent() -> None:
    with TemporaryDirectory() as directory:
        source_path = _write_specification(
            directory,
            "repeat_specification.txt",
            _VALID_SPECIFICATION,
        )

        pipeline = SpecificationPipeline()

        first_result = pipeline.run(source_path)
        second_result = pipeline.run(source_path)

        assert first_result is not second_result
        assert first_result.parse_result is not second_result.parse_result
        assert first_result.semantic_result is not second_result.semantic_result
        assert (
            first_result.validation_result
            is not second_result.validation_result
        )
        assert first_result.specification is not second_result.specification
        assert first_result.diagnostics == second_result.diagnostics
        assert first_result.specification == second_result.specification


def test_pipeline_accepts_an_explicit_empty_rule_set() -> None:
    with TemporaryDirectory() as directory:
        source_path = _write_specification(
            directory,
            "no_rules_specification.txt",
            _VALID_SPECIFICATION,
        )

        pipeline = SpecificationPipeline(rules=())
        result = pipeline.run(source_path)

        assert pipeline.rules == ()
        assert result.validation_result.executed_rule_count == 0
        assert result.validation_result.diagnostics == ()
        assert result.is_successful


def main() -> None:
    tests = (
        test_valid_pipeline_result_maps_and_validates_specification,
        test_pipeline_aggregates_diagnostics_in_phase_order,
        test_validation_receives_semantic_builder_specification,
        test_repeated_pipeline_runs_are_deterministic_and_independent,
        test_pipeline_accepts_an_explicit_empty_rule_set,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nValidated specification-pipeline tests passed.")


if __name__ == "__main__":
    main()
